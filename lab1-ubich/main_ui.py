# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Mon Mar  7 21:00:27 2022
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(787, 573)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(90, 300, 611, 171))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.msg_decrypt_text_edit = QtWidgets.QPlainTextEdit(
            self.layoutWidget)
        self.msg_decrypt_text_edit.setObjectName("msg_decrypt_text_edit")
        self.verticalLayout_2.addWidget(self.msg_decrypt_text_edit)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.decrypt_button = QtWidgets.QPushButton(self.layoutWidget)
        self.decrypt_button.setObjectName("decrypt_button")
        self.horizontalLayout_2.addWidget(self.decrypt_button)
        self.decrypt_save_button = QtWidgets.QPushButton(self.layoutWidget)
        self.decrypt_save_button.setObjectName("decrypt_save_button")
        self.horizontalLayout_2.addWidget(self.decrypt_save_button)
        self.decrypt_load_button = QtWidgets.QPushButton(self.layoutWidget)
        self.decrypt_load_button.setObjectName("decrypt_load_button")
        self.horizontalLayout_2.addWidget(self.decrypt_load_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(570, 510, 201, 22))
        self.label_3.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(90, 20, 611, 205))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.msg_encrypt_text_edit = QtWidgets.QTextEdit(self.layoutWidget1)
        self.msg_encrypt_text_edit.setObjectName("msg_encrypt_text_edit")
        self.verticalLayout.addWidget(self.msg_encrypt_text_edit)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.keyword = QtWidgets.QLineEdit(self.layoutWidget1)
        self.keyword.setObjectName("keyword")
        self.verticalLayout_3.addWidget(self.keyword)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.encrypt_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.encrypt_button.setObjectName("encrypt_button")
        self.horizontalLayout.addWidget(self.encrypt_button)
        self.encrypt_save_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.encrypt_save_button.setObjectName("encrypt_save_button")
        self.horizontalLayout.addWidget(self.encrypt_save_button)
        self.encrypt_load_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.encrypt_load_button.setObjectName("encrypt_load_button")
        self.horizontalLayout.addWidget(self.encrypt_load_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 787, 21))
        self.menubar.setObjectName("menubar")
        self.menu_more = QtWidgets.QMenu(self.menubar)
        self.menu_more.setObjectName("menu_more")
        self.menuHelp = QtWidgets.QMenu(self.menu_more)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.action_author = QtWidgets.QAction(MainWindow)
        self.action_author.setObjectName("action_author")
        self.action_info = QtWidgets.QAction(MainWindow)
        self.action_info.setObjectName("action_info")
        self.actionAlphabets = QtWidgets.QAction(MainWindow)
        self.actionAlphabets.setObjectName("actionAlphabets")
        self.actionConstraints = QtWidgets.QAction(MainWindow)
        self.actionConstraints.setObjectName("actionConstraints")
        self.actionHow_to_use = QtWidgets.QAction(MainWindow)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.menuHelp.addAction(self.actionAlphabets)
        self.menuHelp.addAction(self.actionConstraints)
        self.menuHelp.addAction(self.actionHow_to_use)
        self.menu_more.addAction(self.menuHelp.menuAction())
        self.menu_more.addAction(self.action_author)
        self.menu_more.addAction(self.action_info)
        self.menubar.addAction(self.menu_more.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate(
            "MainWindow", "Ubich Cipher", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Message to Decrypt", None, -1))
        self.decrypt_button.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Decrypt", None, -1))
        self.decrypt_save_button.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Save To file", None, -1))
        self.decrypt_load_button.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Load From File", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Created by Pawel Koch", None, -1))
        self.label.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Message to Encrypt", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Keyword", None, -1))
        self.encrypt_button.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Encrypt", None, -1))
        self.encrypt_save_button.setText(
            QtWidgets.QApplication.translate("MainWindow", "SaveTo File", None, -1))
        self.encrypt_load_button.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Load From File", None, -1))
        self.menu_more.setTitle(QtWidgets.QApplication.translate(
            "MainWindow", "&More", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate(
            "MainWindow", "Help", None, -1))
        self.actionHelp.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Help", None, -1))
        self.action_author.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Author", None, -1))
        self.action_info.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Info", None, -1))
        self.actionAlphabets.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Alphabets", None, -1))
        self.actionConstraints.setText(QtWidgets.QApplication.translate(
            "MainWindow", "Constraints", None, -1))
        self.actionHow_to_use.setText(QtWidgets.QApplication.translate(
            "MainWindow", "How to use?", None, -1))
