from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QGuiApplication

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
        self.setAcceptDrops(True)

        settings_manager = SettingsManager()
        settings_manager.load_window_state(self)

        current_geometry = self.frameGeometry()
        if not any(screen.availableGeometry().contains(current_geometry.topLeft())
                   for screen in QGuiApplication.screens()):
            self.center_window()

        self.splitter = self.ui.splitter
        self.ui.plainTextEdit_main.setMinimumHeight(50)
        self.ui.textEdit_prompt.setMinimumHeight(0)
        if not self.ui.checkBox_prompt.isChecked():
            self.splitter.setSizes([0, self.splitter.size().height()])
        self.ui.textEdit_prompt.setAcceptDrops(False)
        self.ui.plainTextEdit_main.setAcceptDrops(False)

        self.ui.label_project_root.setVisible(False)
        self.ui.lineEdit_project_root.setVisible(False)

        self.overlay = OverlayWidget(self.ui.centralwidget)
        self.overlay.resize(self.ui.centralwidget.size())
        self.ui.centralwidget.installEventFilter(self)

        self.highlighter = MarkdownHighlighter(self.ui.textEdit_prompt.document())

        self.splitter.splitterMoved.connect(self.on_splitter_moved)

        self.presenter = None

    def center_window(self):
        screen = self.screen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def closeEvent(self, event):
        settings_manager = SettingsManager()
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
