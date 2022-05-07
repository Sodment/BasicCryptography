import random
import numpy as np
from PIL import Image
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap, QImage
from main_ui import Ui_MainWindow
import sys

description = '''Simple Visual cryptography, every uploaded image is converted into black-white using threshholding and then split into subpixels on random basis
each splitted pixel is then placed into new image thus creting two images that when placed on top of each other (removing noise required) 
will result in orignal image'''


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, desc):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.desc = desc
        self.image = ''
        self.image_raw = None

        self.ui.encrypt_button.clicked.connect(self.ui_encrypt)
        self.ui.path_to_image.clicked.connect(self.load_from_file_image)
        self.ui.action_author.triggered.connect(self.message_box_author)
        self.ui.action_info.triggered.connect(self.message_box_information)
        self.ui.actionConstraints.triggered.connect(
            self.message_box_constraints)
        self.ui.actionHow_to_use.triggered.connect(self.message_box_hellp)
        self.ui.actionAlphabets.triggered.connect(self.message_box_alphabets)

    def pil2pixmap(self, im):

        if im.mode == "RGB":
            r, g, b = im.split()
            im = Image.merge("RGB", (b, g, r))
        elif im.mode == "RGBA":
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        elif im.mode == "L":
            im = im.convert("RGBA")
        # Bild in RGBA konvertieren, falls nicht bereits passiert
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QImage(
            data, im.size[0], im.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

    def load_from_file_image(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption='Open file', dir='.', filter='*.png;; *.jpg')

        self.image = filename

        self.image_raw = Image.open(filename)
        self.image_raw = self.image_raw.convert('L')
        self.image_raw = self.image_raw.point(lambda p: 255 if p > 127 else 0)
        self.image_raw = self.image_raw.convert('1')

        pixmap = self.pil2pixmap(self.image_raw)
        self.ui.image_shower.setPixmap(pixmap)
        self.ui.image_shower.repaint()

    def ui_encrypt(self):
        if self.image == '':
            QtWidgets.QMessageBox.critical(
                self, "ERROR!", "NO IMAGE SELECTED")
        else:
            self.Encode()

            self.ui.image_shower_2.setPixmap(
                QPixmap("./lab6-visual_cryptography/first_part.png"))
            self.ui.image_shower_2.repaint()
            self.ui.image_shower_3.setPixmap(
                QPixmap("./lab6-visual_cryptography/second_part.png"))
            self.ui.image_shower_3.repaint()

            QtWidgets.QMessageBox.information(
                self, "Succes!", "Message encrypted in two shown images!")

    def message_box_author(self):
        QtWidgets.QMessageBox.information(
            self, "Author", "Created by Paweł Koch")

    def message_box_information(self):
        QtWidgets.QMessageBox.information(
            self, "Informations", self.desc)

    def message_box_hellp(self):
        QtWidgets.QMessageBox.information(
            self, "Help", '''To encrypt just upload an imag and press encrypt button (for bigger images it might take a while)''')

    def message_box_alphabets(self):
        QtWidgets.QMessageBox.information(
            self, "Alphabets", '''It supports all images that are convertible to 1 bit colors (pretty much every image format)''')

    def message_box_constraints(self):
        QtWidgets.QMessageBox.information(
            self, "Constraints", '''Images in 4k migth take even 2 hours to encrypt!''')

    def Encode(self):

        width, height = self.image_raw.size
        array = np.array(list(self.image_raw.getdata()))

        if self.image_raw.mode == 'RGB':
            n = 3
        elif self.image_raw.mode == 'RGBA':
            n = 4
        else:
            n = 1
        total_pixels = array.size//n

        mat_0 = [
            [[0, 1], [0, 1]], [[1, 0], [1, 0]]
        ]

        mat_1 = [
            [[1, 0], [0, 1]], [[0, 1], [1, 0]]
        ]

        img_first = []
        img_second = []

        for p in range(total_pixels):
            mat_to_pick = random.randint(0, 1)
            second_mat = 1 - mat_to_pick
            if array[p] == 255:
                img_first.append(mat_0[mat_to_pick])
                img_second.append(mat_1[second_mat])
            else:
                img_first.append(mat_0[mat_to_pick])
                img_second.append(mat_1[second_mat])

        array_1 = np.array(img_first)
        array_2 = np.array(img_second)

        array_1 = np.squeeze(array_1.reshape(height*2, width*2, n), axis=2)
        array_2 = np.squeeze(array_2.reshape(height*2, width*2, n), axis=2)
        enc_img_first_part = Image.fromarray(
            array_1.astype('bool'))
        enc_img_second_part = Image.fromarray(
            array_2.astype('bool'))
        enc_img_first_part.save("./lab6-visual_cryptography/first_part.png")
        enc_img_second_part.save("./lab6-visual_cryptography/second_part.png")
        print("Image Encoded Successfully")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(description)
    window.show()

    sys.exit(app.exec_())
