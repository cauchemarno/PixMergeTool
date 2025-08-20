from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QGraphicsOpacityEffect, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QGuiApplication, QFontMetrics

from views import Ui_MainWindow
from models import MarkdownHighlighter, SettingsManager


class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")
        self.label = QLabel("Drop your files or folders here", self)
        self.label.setStyleSheet("color: white; font-size: 24px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(self.size())
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.hide()

    def resizeEvent(self, event):
        self.label.resize(self.size())
        super().resizeEvent(event)

    def set_message(self, message):
        self.label.setText(message)

    def show_overlay(self, message=None):
        if message:
            self.set_message(message)
        self.animation.stop()
        self.effect.setOpacity(1)
        self.show()

    def hide_overlay(self):
        self.hide()

    def show_temporary_message(self, message, duration=500):
        self.show_overlay(message)
        QTimer.singleShot(duration, self.fade_out)

    def fade_out(self):
        self.animation.stop()
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        self.animation.finished.connect(self.hide_overlay)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.splitter = self.ui.splitter

        self._stat_words = QLabel("Words: 0")
        self._stat_chars_no_ws = QLabel("Characters (no spaces): 0")
        self._stat_chars_ws = QLabel("Characters: 0")
        self._stat_lines = QLabel("Lines: 0")

        fm = QFontMetrics(self.font())
        for lab, sample in [
            (self._stat_words, "Words: 0000000"),
            (self._stat_chars_no_ws, "Characters (no spaces): 0000000"),
            (self._stat_chars_ws, "Characters: 0000000"),
            (self._stat_lines, "Lines: 0000000"),
        ]:
            lab.setMinimumWidth(fm.horizontalAdvance(sample))
            lab.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self._stat_container = QWidget(self)
        hl = QHBoxLayout(self._stat_container)

        left_pad = max(6, self.logicalDpiX() // 16)
        hl.setContentsMargins(left_pad, 0, 0, 0)

        hl.setSpacing(0)

        def make_sep():
            s = QLabel("|", self._stat_container)
            s.setStyleSheet("padding: 0 8px")
            s.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            return s

        items = [
            self._stat_words,
            self._stat_chars_no_ws,
            self._stat_chars_ws,
            self._stat_lines
        ]
        for i, w in enumerate(items):
            hl.addWidget(w)
            if i < len(items) - 1:
                hl.addWidget(make_sep())

        self.statusBar().addWidget(self._stat_container, 0)
        self.statusBar().setStyleSheet("QStatusBar::item { border: none; }")

        self.setAcceptDrops(True)

        settings_manager = SettingsManager()
        settings_manager.load(self)
        settings_manager.load_window_state(self)

        current_geometry = self.frameGeometry()
        if not any(screen.availableGeometry().contains(current_geometry.topLeft())
                   for screen in QGuiApplication.screens()):
            self.center_window()

        self.ui.plainTextEdit_main.setMinimumHeight(50)
        self.ui.textEdit_prompt.setMinimumHeight(0)

        self.ui.textEdit_prompt.setAcceptDrops(False)
        self.ui.plainTextEdit_main.setAcceptDrops(False)

        self.overlay = OverlayWidget(self.ui.centralwidget)
        self.overlay.resize(self.ui.centralwidget.size())
        self.ui.centralwidget.installEventFilter(self)

        self.highlighter = MarkdownHighlighter(self.ui.textEdit_prompt.document())

        self.splitter.splitterMoved.connect(self.on_splitter_moved)

        self._apply_top_controls_visibility_from_checkbox()

        self.presenter = None

    def _apply_top_controls_visibility_from_checkbox(self):
        checked = self.ui.checkBox_prompt.isChecked()
        if hasattr(self.ui, "button_clear_prompt"):
            self.ui.button_clear_prompt.setVisible(checked)
        if hasattr(self.ui, "button_clear"):
            self.ui.button_clear.setVisible(checked)
        if hasattr(self.ui, "button_clear_main"):
            self.ui.button_clear_main.setVisible(True)

    def center_window(self):
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def closeEvent(self, event):
        settings_manager = SettingsManager()
        settings_manager.save(self)
        settings_manager.save_window_state(self)
        super().closeEvent(event)

    def resizeEvent(self, event):
        self.overlay.resize(self.ui.centralwidget.size())
        super().resizeEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.overlay.show_overlay("Drop your files or folders here")
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.overlay.hide_overlay()
        event.accept()

    def dropEvent(self, event):
        self.overlay.hide_overlay()
        file_urls = event.mimeData().urls()
        file_paths = [url.toLocalFile() for url in file_urls]
        if self.presenter:
            self.presenter.handle_dropped_items(file_paths)
        event.acceptProposedAction()

    def on_splitter_moved(self):
        sizes = self.splitter.sizes()
        total = sum(sizes)
        if self.ui.checkBox_prompt.isChecked():
            new_sizes = sizes.copy()
            changed = False
            if new_sizes[0] < 50:
                new_sizes[0] = 50
                new_sizes[1] = total - 50
                changed = True
            if new_sizes[1] < 50:
                new_sizes[1] = 50
                new_sizes[0] = total - 50
                changed = True
            if changed:
                self.splitter.setSizes(new_sizes)
        else:
            if sizes[1] < 50:
                self.splitter.setSizes([total - 50, 50])

    def set_status_metrics(self, words: int, chars_no_ws: int, chars_ws: int, lines: int):
        self._stat_words.setText(f"Words: {words}")
        self._stat_chars_no_ws.setText(f"Characters (no spaces): {chars_no_ws}")
        self._stat_chars_ws.setText(f"Characters: {chars_ws}")
        self._stat_lines.setText(f"Lines: {lines}")

    def set_always_on_top(self, enabled: bool):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, enabled)
        self.show()
        self.raise_()
        self.activateWindow()
