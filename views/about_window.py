from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.resize(300, 150)
        layout = QVBoxLayout(self)

        about_label = QLabel(self)
        about_label.setOpenExternalLinks(True)
        about_label.setText(
            "<h2>🧩 Pix Merge Tool</h2>"
            "<p>v1.0.0</p>"
            "<p>PixMergeTool merges multiple text/code files into one and generates ASCII folder trees — perfect for sharing and analyzing projects with AI.</p>"
            "<p>Check <a href='https://github.com/cauchemarno/PixMergeTool'>GitHub repository</a> for more information.</p>"
            "<p>App logo is an emoji graphic from <a href='https://github.com/twitter/twemoji'>Twemoji</a> by Twitter(X), "
            "used under <a href='https://creativecommons.org/licenses/by/4.0/'>CC BY 4.0</a>.</p>"
        )
        about_label.setWordWrap(True)
        layout.addWidget(about_label)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
