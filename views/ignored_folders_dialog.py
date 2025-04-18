from PySide6.QtWidgets import QDialog, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel

DEFAULT_IGNORED_FOLDERS = [
    ".idea", ".vscode", ".venv", ".env", "venv", "env", "__pycache__",
    ".mypy_cache", ".pytest_cache", ".git", "node_modules", "dist",
    "build", "target", "out", ".next", ".expo", ".turbo", ".cache", ".coverage"
]


class IgnoredFoldersDialog(QDialog):
    def __init__(self, ignored_folders, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Ignored Folders")
        self.resize(400, 300)
        self.ignored_folders = ignored_folders if ignored_folders else DEFAULT_IGNORED_FOLDERS.copy()

        self.label = QLabel("Ignored Folders:", self)
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(self.ignored_folders)
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Enter folder name...")
        self.add_button = QPushButton("Add", self)
        self.remove_button = QPushButton("Remove Selected", self)
        self.reset_button = QPushButton("Reset", self)
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.add_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_folder)
        self.remove_button.clicked.connect(self.remove_selected)
        self.reset_button.clicked.connect(self.reset_to_default)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def add_folder(self):
        folder = self.input_line.text().strip()
        if folder and folder not in self.ignored_folders:
            self.ignored_folders.append(folder)
            self.list_widget.addItem(folder)
            self.input_line.clear()

    def remove_selected(self):
        for item in self.list_widget.selectedItems():
            self.ignored_folders.remove(item.text())
            self.list_widget.takeItem(self.list_widget.row(item))

    def reset_to_default(self):
        self.ignored_folders = DEFAULT_IGNORED_FOLDERS.copy()
        self.list_widget.clear()
        self.list_widget.addItems(self.ignored_folders)

    def get_ignored_folders(self):
        return self.ignored_folders
