import numpy as np
from PIL import Image
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap
from main_ui import Ui_MainWindow
import sys

description = '''Ubchi jest szyfrem dwukrotnego przestawienia kolumnowego stosowanym przez niemcow podczas I Wojny światowej do przekazywania informacji. Do zaszyfrowania wiadomosci tą metodą potrzebujemy słowa/zdania kluczowego. Szyfrowanie odbywa sie poprzez numerowanie liter słowa kluczowego w porzadku alfabetycznym (litery powtarzajace sie były numerowane od lewej do prawej) a nastepnie wykonaniu szesciu krokow zwiazanych z przestawieniami w tabeli Deszyfrowanie to wykonanie krokow szyfrowania w odwrotnej kolejnosci'''


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, desc):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.desc = desc
        self.image = ''

        self.ui.encrypt_button.clicked.connect(self.ui_encrypt)
        self.ui.decrypt_button.clicked.connect(self.ui_decrypt)
        self.ui.path_to_image.clicked.connect(self.load_from_file_image)
        self.ui.load_message_button.clicked.connect(
            self.load_from_file_message)
        self.ui.action_author.triggered.connect(self.message_box_author)
        self.ui.action_info.triggered.connect(self.message_box_information)
        self.ui.actionConstraints.triggered.connect(
            self.message_box_constraints)
        self.ui.actionHow_to_use.triggered.connect(self.message_box_hellp)
        self.ui.actionAlphabets.triggered.connect(self.message_box_alphabets)

    def load_from_file_image(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Open file', dir='.', filter='*.png')

        self.image = filename

        pixmap = QPixmap(filename)
        self.ui.image_shower.setPixmap(pixmap)
        self.ui.image_shower.repaint()

    def load_from_file_message(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Open file', dir='.', filter='*.txt')

        with open(filename, 'r', encoding='utf-8') as file:
            self.ui.message_textfield.setPlainText(file.read())

    def ui_encrypt(self):
        if self.image == '':
            QtWidgets.QMessageBox.critical(
                self, "ERROR!", "NO IMAGE SELECTED")
        else:
            text_to_encrypt = self.ui.message_textfield.toPlainText()
            Encode(self.image, text_to_encrypt)
            QtWidgets.QMessageBox.information(
                self, "Succes!", "Message encrypted in image")

    def ui_decrypt(self):
        if self.image == '':
            QtWidgets.QMessageBox.critical(
                self, "ERROR!", "NO IMAGE SELECTED")
        else:
            try:
                self.ui.message_textfield.setPlainText(Decode(self.image))
                QtWidgets.QMessageBox.information(
                    self, "Succes!", "Message decrypted!")
            except ZeroDivisionError:
                QtWidgets.QMessageBox.critical(
                    self, "ERROR!", "No hidden message found!")

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


def Encode(src, message):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    message += "$t3g0"

    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(
                        bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

    array = array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(src)
    print("Image Encoded Successfully")


def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        return message[:-5]
    else:
        raise ZeroDivisionError


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(description)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
