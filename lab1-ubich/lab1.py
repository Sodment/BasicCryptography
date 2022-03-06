import random
import string
import numpy as np
import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
#Moj Szyfr
#ubchi
#skany 023 i 024

def round_of_ubich(keyword, text):
    mat = np.array([ch for ch in keyword+text])
    mat.resize(len(text)//len(keyword)+ 2, len(keyword))
    mat.reshape((-1, len(keyword)))
    print(f'Krok 1: \n{mat}')
    mat = mat[:, mat[0].argsort()]
    print(f'Krok 2: \n{mat}')
    mat = np.delete(mat,(0), axis=0)
    print(f'Krok 3: \n{mat}')
    mat = np.transpose(mat)
    arr = mat.flatten('C')
    print(f'Krok 4: \n{arr}')
    arr = ''.join(ch for ch in arr)
    return arr

def round_of_ubich_decrypt(keyword, text):
    print([])
    mat = np.array(sorted([ch for ch in keyword]) + [ch for ch in text])
    mat.resize(len(text)//len(keyword)+ 2, len(keyword))
    mat.reshape((-1, len(keyword)))
    print(f'Krok 1: \n{mat}')
    print([keyword.index(mat[0, 0:][i]) for i in range(len(keyword))])
    #mat = mat[:, [keyword.index(mat[0][i]) for i in mat[0]]]
    print(mat)


def encrypt(keyword, text):
    text = str(text).upper()
    words_in_keyword = len(str(keyword).split())
    first_round = round_of_ubich(keyword, text)
    null_letters = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(words_in_keyword))
    first_round = first_round + null_letters
    second_round = round_of_ubich(keyword, first_round)
    print(f'Encrypted message: {second_round}')
    return second_round


def decrypt(keyword, text):
    text = str(text).upper()
    words_in_keyword = len(str(keyword).split())
    round_of_ubich_decrypt(keyword, text)

def set_UI(window: QUiLoader):
    window.encrypt_load_button.clicked.connect(encrypt("UBER", "SECRET"))
    dialog = window.


def ui(desc,encryption=encrypt, decryption=decrypt):
    loader = QUiLoader()
    app = QtWidgets.QApplication(sys.argv)
    window = loader.load("mainwindow.ui", None)
    set_UI(window)
    window.show()
    app.exec_()

def main():
    #encrypt('UBER', 'SECRET')
    #decrypt('UBER', 'TECMRES')
    ui('xd')

if __name__ == '__main__':
    main()