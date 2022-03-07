from decimal import DivisionByZero
from msilib.schema import Error
import sys
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from main_ui import Ui_MainWindow
from ubich import encrypt, decrypt
# Moj Szyfr
# ubchi
# skany 023 i 024
description = '''Ubchi jest szyfrem dwukrotnego przestawienia kolumnowego stosowanym przez niemcow podczas I Wojny światowej do przekazywania informacji. Do zaszyfrowania wiadomosci tą metodą potrzebujemy słowa/zdania kluczowego. Szyfrowanie odbywa sie poprzez numerowanie liter słowa kluczowego w porzadku alfabetycznym (litery powtarzajace sie były numerowane od lewej do prawej) a nastepnie wykonaniu szesciu krokow zwiazanych z przestawieniami w tabeli Deszyfrowanie to wykonanie krokow szyfrowania w odwrotnej kolejnosci'''


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, desc):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.desc = desc

        self.ui.encrypt_button.clicked.connect(self.ui_encrypt)
        self.ui.decrypt_button.clicked.connect(self.ui_decrypt)
        self.ui.encrypt_load_button.clicked.connect(
            self.load_from_file_encrypt)
        self.ui.decrypt_load_button.clicked.connect(
            self.load_from_file_decrypt)
        self.ui.encrypt_save_button.clicked.connect(
            self.save_to_file_encrypt)
        self.ui.decrypt_save_button.clicked.connect(
            self.save_to_file_decrypt)
        self.ui.action_author.triggered.connect(self.message_box_author)
        self.ui.action_info.triggered.connect(self.message_box_information)
        self.ui.actionConstraints.triggered.connect(
            self.message_box_constraints)
        self.ui.actionHow_to_use.triggered.connect(self.message_box_hellp)
        self.ui.actionAlphabets.triggered.connect(self.message_box_alphabets)

    def load_from_file_encrypt(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Open file', dir='.', filter='*.txt')

        with open(filename, 'r', encoding='utf-8') as file:
            self.ui.msg_encrypt_text_edit.setPlainText(file.read())

    def load_from_file_decrypt(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Open file', dir='.', filter='*.txt')

        with open(filename, 'r', encoding='utf-8') as file:
            self.ui.msg_decrypt_text_edit.setPlainText(file.read())

    def save_to_file_decrypt(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Choose File to save', dir='.', filter='*.txt')

        with open(filename, 'w', encoding='utf-8') as file:
            text = self.ui.msg_decrypt_text_edit.toPlainText()
            file.write(text)

    def save_to_file_encrypt(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Choose File to save', dir='.', filter='*.txt')

        with open(filename, 'w', encoding='utf-8') as file:
            text = self.ui.msg_encrypt_text_edit.toPlainText()
            file.write(text)

    def ui_encrypt(self):
        try:
            text_to_encrypt = self.ui.msg_encrypt_text_edit.toPlainText()
            text_keyword = self.ui.keyword.text()
            if len(text_keyword) == 0 or len(text_to_encrypt) == 0 or len(text_keyword) > 15:
                raise ZeroDivisionError
            try:
                encrypted_message = encrypt(text_keyword, text_to_encrypt)
            except ZeroDivisionError:
                QtWidgets.QMessageBox.critical(
                    self, "ERROR!", "Missing message to encrypt")
            self.ui.msg_decrypt_text_edit.setPlainText(encrypted_message)
        except ZeroDivisionError:
            QtWidgets.QMessageBox.critical(
                self, "ERROR!", "Missing required field!")

    def ui_decrypt(self):
        try:
            text_to_decrypt = self.ui.msg_decrypt_text_edit.toPlainText()
            text_keyword = self.ui.keyword.text()
            if len(text_keyword) == 0 or len(text_to_decrypt) == 0 or len(text_keyword) > 15:
                raise ZeroDivisionError
            try:
                decrypted_message = decrypt(text_keyword, text_to_decrypt)
            except ZeroDivisionError:
                QtWidgets.QMessageBox.critical(
                    self, "ERROR!", "Missing message to decrypt")
            self.ui.msg_encrypt_text_edit.setPlainText(decrypted_message)
        except ZeroDivisionError:
            QtWidgets.QMessageBox.critical(
                self, "ERROR!", "Missing required field or keyword is too long!")

    def message_box_author(self):
        QtWidgets.QMessageBox.information(
            self, "Author", "Created by Paweł Koch")

    def message_box_information(self):
        QtWidgets.QMessageBox.information(
            self, "Informations", self.desc)

    def message_box_hellp(self):
        QtWidgets.QMessageBox.information(
            self, "Help", '''To encrypt/decrypt a message just use the text fields to input the text and Keyword field to input a valid keywordthen press the Encrypt/Decrypt button and the encrypted/decrypted message will pop up in counter-field,ie. encrypted message by use of ecnrypt button wil pop up in decrypt text field.You can also load message to encrypt/decrypt from .txt file by ussing adequate button''')

    def message_box_alphabets(self):
        QtWidgets.QMessageBox.information(self, "Alphabets", '''Program support all kinds of alphabets that are supported by UTF-8 encoding,
        a large amount of whitespaces can obscure the prcoess, use of char - and ~ may result in failure due to internal system
        program was tested against german, polish, english, chinese and emoji alphabets containig 20-30 words''')

    def message_box_constraints(self):
        QtWidgets.QMessageBox.information(self, "Constraints", '''Keyword shnould not belonger than 15 characters including special characters,
        The message to encrypt/decrypt was tested against very long texts eg. lorem ipsum or Pan Tadeusz, Max numbers of characters to encrypt/decrypt is around  2**16''')


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(description)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
