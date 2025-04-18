from PySide6.QtCore import QSettings


class SettingsManager:
    def __init__(self):
        self.settings = QSettings("cauchemarno", "PixMergeTool")

    def _save_value(self, key, value):
        self.settings.setValue(key, value)

    def _load_value(self, key, default, value_type):
        return self.settings.value(key, default, type=value_type)

    def save(self, view):
        ui = view.ui
        self._save_value("prompt_enabled", ui.checkBox_prompt.isChecked())

        persist_fields = ui.action_persist_fields.isChecked() if hasattr(ui, "action_persist_fields") else True
        self._save_value("persist_fields", persist_fields)
        if persist_fields:
            self._save_value("textEdit_prompt", ui.textEdit_prompt.toPlainText())
            self._save_value("plainTextEdit_main", ui.plainTextEdit_main.toPlainText())
            self._save_value("lineEdit_project_root", ui.lineEdit_project_root.text())
        else:
            self.settings.remove("textEdit_prompt")
            self.settings.remove("plainTextEdit_main")
            self.settings.remove("lineEdit_project_root")

        format_value = "markdown" if ui.action_markdown.isChecked() else "xml"
        self._save_value("format", format_value)

        if ui.action_filename_only.isChecked():
            self._save_value("path_style", "filename")
        elif ui.action_fullpath.isChecked():
            self._save_value("path_style", "full")
        elif ui.action_relative.isChecked():
            self._save_value("path_style", "relative")
            self._save_value("project_root", ui.lineEdit_project_root.text().strip())
        else:
            self._save_value("path_style", "filename")
            self.settings.remove("project_root")

        self._save_value("show_ignored", ui.action_show_ignored.isChecked())
        self._save_value("add_language", ui.action_add_language.isChecked())
        self._save_value("append_mode", ui.action_append.isChecked())

        if hasattr(view, 'splitter') and ui.checkBox_prompt.isChecked():
            self._save_value("splitter_state", view.splitter.saveState())

    def load(self, view):
        ui = view.ui
        prompt_enabled = self._load_value("prompt_enabled", False, bool)
        try:
            ui.checkBox_prompt.blockSignals(True)
            ui.checkBox_prompt.setChecked(prompt_enabled)
        finally:
            ui.checkBox_prompt.blockSignals(False)

        ui.textEdit_prompt.setVisible(prompt_enabled)

        persist_fields = self._load_value("persist_fields", True, bool)
        if hasattr(ui, "action_persist_fields"):
            ui.action_persist_fields.setChecked(persist_fields)
        if persist_fields:
            ui.textEdit_prompt.setPlainText(self._load_value("textEdit_prompt", "", str))
            ui.plainTextEdit_main.setPlainText(self._load_value("plainTextEdit_main", "", str))
            ui.lineEdit_project_root.setText(self._load_value("lineEdit_project_root", "", str))
        else:
            ui.textEdit_prompt.clear()
            ui.plainTextEdit_main.clear()
            ui.lineEdit_project_root.clear()

        format_value = self._load_value("format", "markdown", str)
        if format_value == "markdown":
            ui.action_markdown.setChecked(True)
            ui.action_xml.setChecked(False)
        else:
            ui.action_markdown.setChecked(False)
            ui.action_xml.setChecked(True)

        path_style = self._load_value("path_style", "filename", str)
        if path_style == "filename":
            ui.action_filename_only.setChecked(True)
            ui.action_fullpath.setChecked(False)
            ui.action_relative.setChecked(False)
            ui.label_project_root.setVisible(False)
            ui.lineEdit_project_root.setVisible(False)
        elif path_style == "full":
            ui.action_fullpath.setChecked(True)
            ui.action_filename_only.setChecked(False)
            ui.action_relative.setChecked(False)
            ui.label_project_root.setVisible(False)
            ui.lineEdit_project_root.setVisible(False)
        elif path_style == "relative":
            ui.action_relative.setChecked(True)
            ui.action_filename_only.setChecked(False)
            ui.action_fullpath.setChecked(False)
            ui.label_project_root.setVisible(True)
            ui.lineEdit_project_root.setVisible(True)
            project_root = self._load_value("project_root", "", str)
            ui.lineEdit_project_root.setText(project_root)
        else:
            ui.action_filename_only.setChecked(True)

        ui.action_show_ignored.setChecked(self._load_value("show_ignored", True, bool))
        ui.action_add_language.setChecked(self._load_value("add_language", True, bool))
        ui.action_append.setChecked(self._load_value("append_mode", False, bool))

        if hasattr(view, 'splitter'):
            if prompt_enabled:
                splitter_state = self.settings.value("splitter_state", None)
                if splitter_state is not None:
                    view.splitter.restoreState(splitter_state)
                else:
                    total = view.splitter.size().height()
                    half = total // 2 if total >= 100 else 50
                    view.splitter.setSizes([half, total - half])
                view.splitter.setCollapsible(0, False)
            else:
                total = view.splitter.size().height()
                view.splitter.setSizes([0, total])
                view.splitter.setCollapsible(0, True)
            if prompt_enabled:
                ui.textEdit_prompt.setMinimumHeight(50)
            else:
                ui.textEdit_prompt.setMinimumHeight(0)

    def save_ignored_folders(self, ignored_folders):
        self.settings.setValue("ignored_folders", ignored_folders)

    def load_ignored_folders(self):
        default = [
            ".idea", ".vscode", ".venv", ".env", "venv", "env", "__pycache__",
            ".mypy_cache", ".pytest_cache", ".git", "node_modules", "dist",
            "build", "target", "out", ".next", ".expo", ".turbo", ".cache", ".coverage"
        ]
        if self.settings.contains("ignored_folders"):
            folders = self.settings.value("ignored_folders")
            if not folders:
                return []
            if isinstance(folders, str):
                return [folders]
            return list(folders)
        else:
            return default

    def save_window_state(self, window):
        self._save_value("window_geometry", window.saveGeometry())
        self._save_value("window_state", window.saveState())

    def load_window_state(self, window):
        geometry = self.settings.value("window_geometry")
        state = self.settings.value("window_state")
        if geometry is not None:
            window.restoreGeometry(geometry)
        if state is not None:
            window.restoreState(state)
