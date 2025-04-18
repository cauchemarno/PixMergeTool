import sys
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from views import MainWindow
from presenters import MainPresenter
from models import SettingsManager
from resources import resources_rc


def main():
    app = QApplication(sys.argv)

    if sys.platform.startswith("win"):
        icon_path = ":/resources/icons/icon.ico"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PixMergeTool')
    elif sys.platform.startswith("darwin"):
        icon_path = ":/resources/icons/icon.icns"
    else:
        icon_path = ":/resources/icons/icon.png"

    app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    presenter = MainPresenter(window)

    settings_manager = SettingsManager()
    settings_manager.load(window)

    app.aboutToQuit.connect(lambda: settings_manager.save(window))

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
