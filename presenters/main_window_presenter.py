import os

from PySide6.QtWidgets import QMessageBox, QFileDialog, QApplication, QDialog

from views import AboutWindow, IgnoredFoldersDialog
from models import FileProcessor, SettingsManager


class MainPresenter:
    def __init__(self, view):
        self.view = view
        self.view.presenter = self
        self.processor = FileProcessor()
        self.previous_splitter_sizes = None
        self.setup_connections()

    def setup_connections(self):
        ui = self.view.ui
        ui.checkBox_prompt.toggled.connect(self.toggle_prompt)
        ui.button_copy.clicked.connect(self.copy_to_clipboard)
        ui.button_save.clicked.connect(self.save_to_txt)
        ui.button_clear.clicked.connect(self.clear_text)

        ui.action_markdown.triggered.connect(self.select_markdown)
        ui.action_xml.triggered.connect(self.select_xml)
        ui.action_filename_only.triggered.connect(self.select_filename_only)
        ui.action_fullpath.triggered.connect(self.select_fullpath)
        ui.action_relative.triggered.connect(self.select_relative)
        ui.action_about.triggered.connect(self.show_about)
        if hasattr(ui, "action_edit_ignored"):
            ui.action_edit_ignored.triggered.connect(self.edit_ignored_folders)

        ui.textEdit_prompt.textChanged.connect(self.update_symbol_counter)
        ui.plainTextEdit_main.textChanged.connect(self.update_symbol_counter)

    def toggle_prompt(self, checked: bool):
        splitter = self.view.splitter
        total = splitter.size().height()
        if checked:
            self.view.ui.textEdit_prompt.setVisible(True)
            self.view.ui.textEdit_prompt.setMinimumHeight(50)
            self.view.ui.plainTextEdit_main.setMinimumHeight(50)
            splitter.setCollapsible(0, False)
            splitter.setCollapsible(1, False)
            if self.previous_splitter_sizes is not None and self.previous_splitter_sizes[0] >= 50 and \
                    self.previous_splitter_sizes[1] >= 50:
                sizes = self.previous_splitter_sizes
            else:
                half = total // 2
                if half < 50:
                    half = 50
                sizes = [half, total - half]
            splitter.setSizes(sizes)
        else:
            current_sizes = splitter.sizes()
            if current_sizes[0] >= 50:
                self.previous_splitter_sizes = current_sizes
            self.view.ui.textEdit_prompt.setVisible(False)
            splitter.setCollapsible(0, True)
            splitter.setCollapsible(1, True)
            splitter.setSizes([0, total])
        self.update_symbol_counter()

    def copy_to_clipboard(self):
        full_text = self.get_full_text()
        QApplication.clipboard().setText(full_text)
        self.view.overlay.show_temporary_message("Copied to clipboard", duration=500)

    def save_to_txt(self):
        full_text = self.get_full_text()
        path, _ = QFileDialog.getSaveFileName(self.view, "Save File", filter="Text Files (*.txt)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                self.view.overlay.show_temporary_message("File saved successfully", duration=500)
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Error saving file: {str(e)}")

    def clear_text(self):
        reply = QMessageBox.question(self.view, "Confirm", "Are you sure to clear all?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.view.ui.textEdit_prompt.clear()
            self.view.ui.plainTextEdit_main.clear()
            self.view.ui.lineEdit_project_root.clear()
            self.update_symbol_counter()

    def get_full_text(self) -> str:
        text = ""
        if self.view.ui.checkBox_prompt.isChecked():
            text += self.view.ui.textEdit_prompt.toPlainText() + "\n\n"
        text += self.view.ui.plainTextEdit_main.toPlainText()
        return text

    def update_symbol_counter(self):
        ui = self.view.ui
        if ui.checkBox_prompt.isChecked():
            prompt_text = ui.textEdit_prompt.toPlainText().strip()
        else:
            prompt_text = ""
        main_text = ui.plainTextEdit_main.toPlainText()
        full_text = prompt_text + main_text
        chars = len(full_text)
        ui.label_token_counter.setText(f"Symbols: {chars}")

    def handle_dropped_items(self, paths):
        append_mode = self.view.ui.action_append.isChecked()
        new_text = ""
        for path in paths:
            if os.path.isdir(path) or os.path.isfile(path):
                processed = self.processor.process_file(path, self.get_current_settings())
                if processed is None:
                    QMessageBox.warning(self.view, "Warning",
                        f"File or folder '{path}' is binary or could not be processed.")
                else:
                    new_text += processed + "\n"
        if not append_mode:
            self.view.ui.plainTextEdit_main.setPlainText(new_text)
        else:
            current_text = self.view.ui.plainTextEdit_main.toPlainText()
            combined = current_text + "\n" + new_text if current_text else new_text
            self.view.ui.plainTextEdit_main.setPlainText(combined)
        self.update_symbol_counter()

    def get_current_settings(self) -> dict:
        ui = self.view.ui
        settings = {'format': 'markdown' if ui.action_markdown.isChecked() else 'xml'}
        if ui.action_filename_only.isChecked():
            settings['path_style'] = 'filename'
        elif ui.action_fullpath.isChecked():
            settings['path_style'] = 'full'
        elif ui.action_relative.isChecked():
            settings['path_style'] = 'relative'
            project_root = ui.lineEdit_project_root.text().strip()
            settings['project_root'] = project_root if project_root else None
        else:
            settings['path_style'] = 'filename'
        settings['show_ignored'] = ui.action_show_ignored.isChecked() if hasattr(ui, 'action_show_ignored') else True
        settings['add_language'] = ui.action_add_language.isChecked() if hasattr(ui, 'action_add_language') else True
        return settings

    def select_markdown(self):
        self.view.ui.action_markdown.setChecked(True)
        self.view.ui.action_xml.setChecked(False)

    def select_xml(self):
        self.view.ui.action_xml.setChecked(True)
        self.view.ui.action_markdown.setChecked(False)

    def select_filename_only(self):
        ui = self.view.ui
        ui.action_filename_only.setChecked(True)
        ui.action_fullpath.setChecked(False)
        ui.action_relative.setChecked(False)
        ui.label_project_root.setVisible(False)
        ui.lineEdit_project_root.setVisible(False)

    def select_fullpath(self):
        ui = self.view.ui
        ui.action_fullpath.setChecked(True)
        ui.action_filename_only.setChecked(False)
        ui.action_relative.setChecked(False)
        ui.label_project_root.setVisible(False)
        ui.lineEdit_project_root.setVisible(False)

    def select_relative(self):
        ui = self.view.ui
        ui.action_relative.setChecked(True)
        ui.action_filename_only.setChecked(False)
        ui.action_fullpath.setChecked(False)
        ui.label_project_root.setVisible(True)
        ui.lineEdit_project_root.setVisible(True)

    def show_about(self):
        about = AboutWindow(self.view)
        about.exec()

    def edit_ignored_folders(self):
        settings_manager = SettingsManager()
        current_ignored = settings_manager.load_ignored_folders()
        dialog = IgnoredFoldersDialog(current_ignored, self.view)
        if dialog.exec() == QDialog.Accepted:
            new_list = dialog.get_ignored_folders()
            settings_manager.save_ignored_folders(new_list)
            self.processor.ignored_dirs = set(new_list)
