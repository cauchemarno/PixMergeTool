# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_markdown = QAction(MainWindow)
        self.action_markdown.setObjectName(u"action_markdown")
        self.action_markdown.setCheckable(True)
        self.action_markdown.setChecked(True)
        self.action_xml = QAction(MainWindow)
        self.action_xml.setObjectName(u"action_xml")
        self.action_xml.setCheckable(True)
        self.action_filename_only = QAction(MainWindow)
        self.action_filename_only.setObjectName(u"action_filename_only")
        self.action_filename_only.setCheckable(True)
        self.action_filename_only.setChecked(True)
        self.action_fullpath = QAction(MainWindow)
        self.action_fullpath.setObjectName(u"action_fullpath")
        self.action_fullpath.setCheckable(True)
        self.action_relative = QAction(MainWindow)
        self.action_relative.setObjectName(u"action_relative")
        self.action_relative.setCheckable(True)
        self.action_append = QAction(MainWindow)
        self.action_append.setObjectName(u"action_append")
        self.action_append.setCheckable(True)
        self.action_show_ignored = QAction(MainWindow)
        self.action_show_ignored.setObjectName(u"action_show_ignored")
        self.action_show_ignored.setCheckable(True)
        self.action_show_ignored.setChecked(True)
        self.action_add_language = QAction(MainWindow)
        self.action_add_language.setObjectName(u"action_add_language")
        self.action_add_language.setCheckable(True)
        self.action_add_language.setChecked(True)
        self.action_edit_ignored = QAction(MainWindow)
        self.action_edit_ignored.setObjectName(u"action_edit_ignored")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_prompt_and_clear = QHBoxLayout()
        self.layout_prompt_and_clear.setObjectName(u"layout_prompt_and_clear")
        self.checkBox_prompt = QCheckBox(self.centralwidget)
        self.checkBox_prompt.setObjectName(u"checkBox_prompt")

        self.layout_prompt_and_clear.addWidget(self.checkBox_prompt)

        self.button_clear_prompt = QPushButton(self.centralwidget)
        self.button_clear_prompt.setObjectName(u"button_clear_prompt")

        self.layout_prompt_and_clear.addWidget(self.button_clear_prompt)

        self.button_clear_main = QPushButton(self.centralwidget)
        self.button_clear_main.setObjectName(u"button_clear_main")

        self.layout_prompt_and_clear.addWidget(self.button_clear_main)

        self.button_clear = QPushButton(self.centralwidget)
        self.button_clear.setObjectName(u"button_clear")

        self.layout_prompt_and_clear.addWidget(self.button_clear)

        self.toolbar_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_prompt_and_clear.addItem(self.toolbar_spacer)

        self.button_pin = QPushButton(self.centralwidget)
        self.button_pin.setObjectName(u"button_pin")
        self.button_pin.setCheckable(True)

        self.layout_prompt_and_clear.addWidget(self.button_pin)


        self.verticalLayout.addLayout(self.layout_prompt_and_clear)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.textEdit_prompt = QTextEdit(self.splitter)
        self.textEdit_prompt.setObjectName(u"textEdit_prompt")
        font = QFont()
        font.setPointSize(11)
        self.textEdit_prompt.setFont(font)
        self.textEdit_prompt.setVisible(False)
        self.splitter.addWidget(self.textEdit_prompt)
        self.plainTextEdit_main = QPlainTextEdit(self.splitter)
        self.plainTextEdit_main.setObjectName(u"plainTextEdit_main")
        self.splitter.addWidget(self.plainTextEdit_main)

        self.verticalLayout.addWidget(self.splitter)

        self.layout_project_root = QHBoxLayout()
        self.layout_project_root.setObjectName(u"layout_project_root")
        self.label_project_root = QLabel(self.centralwidget)
        self.label_project_root.setObjectName(u"label_project_root")

        self.layout_project_root.addWidget(self.label_project_root)

        self.lineEdit_project_root = QLineEdit(self.centralwidget)
        self.lineEdit_project_root.setObjectName(u"lineEdit_project_root")

        self.layout_project_root.addWidget(self.lineEdit_project_root)


        self.verticalLayout.addLayout(self.layout_project_root)

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setObjectName(u"layout_buttons")
        self.button_copy = QPushButton(self.centralwidget)
        self.button_copy.setObjectName(u"button_copy")

        self.layout_buttons.addWidget(self.button_copy)

        self.button_save = QPushButton(self.centralwidget)
        self.button_save.setObjectName(u"button_save")

        self.layout_buttons.addWidget(self.button_save)


        self.verticalLayout.addLayout(self.layout_buttons)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menubar.setNativeMenuBar(False)
        self.menuBarLayout = QHBoxLayout(self.menubar)
        self.menuBarLayout.setObjectName(u"menuBarLayout")
        self.menuFormat = QMenu(self.menubar)
        self.menuFormat.setObjectName(u"menuFormat")

        self.menuBarLayout.addWidget(self.menuFormat)

        self.menuFilePath = QMenu(self.menubar)
        self.menuFilePath.setObjectName(u"menuFilePath")

        self.menuBarLayout.addWidget(self.menuFilePath)

        self.menuAppend = QMenu(self.menubar)
        self.menuAppend.setObjectName(u"menuAppend")

        self.menuBarLayout.addWidget(self.menuAppend)

        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")

        self.menuBarLayout.addWidget(self.menuHelp)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFormat.menuAction())
        self.menubar.addAction(self.menuFilePath.menuAction())
        self.menubar.addAction(self.menuAppend.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFormat.addAction(self.action_markdown)
        self.menuFormat.addAction(self.action_xml)
        self.menuFilePath.addAction(self.action_filename_only)
        self.menuFilePath.addAction(self.action_fullpath)
        self.menuFilePath.addAction(self.action_relative)
        self.menuAppend.addAction(self.action_append)
        self.menuAppend.addSeparator()
        self.menuAppend.addAction(self.action_add_language)
        self.menuAppend.addSeparator()
        self.menuAppend.addAction(self.action_show_ignored)
        self.menuAppend.addAction(self.action_edit_ignored)
        self.menuHelp.addAction(self.action_about)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pix Merge Tool", None))
        self.action_markdown.setText(QCoreApplication.translate("MainWindow", u"Markdown", None))
        self.action_xml.setText(QCoreApplication.translate("MainWindow", u"XML", None))
        self.action_filename_only.setText(QCoreApplication.translate("MainWindow", u"Filename only", None))
        self.action_fullpath.setText(QCoreApplication.translate("MainWindow", u"Full path", None))
        self.action_relative.setText(QCoreApplication.translate("MainWindow", u"Relative to project folder", None))
        self.action_append.setText(QCoreApplication.translate("MainWindow", u"Append new files and folders", None))
        self.action_show_ignored.setText(QCoreApplication.translate("MainWindow", u"Show ignored folders in ASCII tree", None))
        self.action_add_language.setText(QCoreApplication.translate("MainWindow", u"Add language to markdown if possible", None))
        self.action_edit_ignored.setText(QCoreApplication.translate("MainWindow", u"Edit ignored folders", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.checkBox_prompt.setText(QCoreApplication.translate("MainWindow", u"Use Custom Prompt", None))
        self.button_clear_prompt.setText(QCoreApplication.translate("MainWindow", u" Clear Prompt ", None))
        self.button_clear_main.setText(QCoreApplication.translate("MainWindow", u" Clear Merge ", None))
        self.button_clear.setText(QCoreApplication.translate("MainWindow", u"Clear All", None))
        self.button_pin.setText(QCoreApplication.translate("MainWindow", u"Pin On Top", None))
        self.textEdit_prompt.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Write your prompt here...", None))
        self.plainTextEdit_main.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Drag & drop files or folders here", None))
        self.label_project_root.setText(QCoreApplication.translate("MainWindow", u"Root folder for relative paths:", None))
        self.lineEdit_project_root.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter folder name to trim from paths...", None))
        self.button_copy.setText(QCoreApplication.translate("MainWindow", u"Copy Result to Clipboard", None))
        self.button_save.setText(QCoreApplication.translate("MainWindow", u"Export as .txt", None))
        self.menuFormat.setTitle(QCoreApplication.translate("MainWindow", u"Code Wrapping", None))
        self.menuFilePath.setTitle(QCoreApplication.translate("MainWindow", u"File Path Display", None))
        self.menuAppend.setTitle(QCoreApplication.translate("MainWindow", u"Merge Behavior", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

