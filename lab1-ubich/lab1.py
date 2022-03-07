import sys
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from main_ui import Ui_MainWindow
from ubich import encrypt, decrypt
# Moj Szyfr
# ubchi
# skany 023 i 024


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.encrypt_button.clicked.connect(self.ui_encrypt)
        self.ui.decrypt_button.clicked.connect(self.ui_decrypt)

    def ui_encrypt(self):
        text_to_encrypt = self.ui.msg_encrypt_text_edit.toPlainText()
        text_keyword = self.ui.keyword.text()
        encrypted_message = encrypt(text_keyword, text_to_encrypt)
        self.ui.msg_decrypt_text_edit.setPlainText(encrypted_message)

    def ui_decrypt(self):
        text_to_decrypt = self.ui.msg_decrypt_text_edit.toPlainText()
        text_keyword = self.ui.keyword.text()
        decrypted_message = decrypt(text_keyword, text_to_decrypt)
        self.ui.msg_encrypt_text_edit.setPlainText(decrypted_message)


def ui(desc, encryption=encrypt, decryption=decrypt):
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


def main():
    # encrypt('DIEWACHTAMRHEIN', 'SECRET')
    # decrypt('DIEWACHTAMRHEIN', encrypt('DIEWACHTAMRHEIN',
    #                                   'Tenth divison X Attack Montigny sector at daylight X Gas barrage to precede you'))
    # decrypt("UBER", encrypt('UBER', "Secret"))
    ui('xd')


if __name__ == '__main__':
    main()
