import random
import string
import numpy as np

def round_of_ubich(keyword, text):
    mat = np.array([ch for ch in keyword+text])
    mat.resize(len(text)//len(keyword) + 2, len(keyword))
    mat.reshape((-1, len(keyword)))
    print(f'Krok 1: \n{mat}')
    mat = mat[:, mat[0].argsort()]
    print(f'Krok 2: \n{mat}')
    mat = np.delete(mat, (0), axis=0)
    print(f'Krok 3: \n{mat}')
    mat = np.transpose(mat)
    arr = mat.flatten('C')
    print(f'Krok 4: \n{arr}')
    arr = ''.join(ch for ch in arr)
    return arr


def round_of_ubich_decrypt(keyword, text):
    mat = np.full((len(text)//len(keyword) + 2, len(keyword)), '~')
    mat[0] = [ch for ch in keyword]
    print(f'Krok 1: \n{mat}')
    k = 0
    empty = ' ' * len(text)
    for i in range(1, len(text)//len(keyword) + 2):
        for j in range(len(keyword)):
            try:

                mat[i, j] = empty[k]
                k += 1
            except IndexError:
                break
    mat = mat[:, mat[0].argsort()]
    print(f'Krok 2: \n{mat}')
    k = 0
    for i in range(len(keyword)):
        for j in range(1, len(text)//len(keyword) + 2):
            try:
                if(mat[j, i] != '~'):
                    mat[j, i] = text[k]
                    k += 1
                else:
                    continue
            except IndexError:
                break
    mat = mat[:, get_original_positions(keyword)]
    print(f'Krok 3: \n{mat}')
    mat = np.delete(mat, (0), axis=0)
    arr = mat.flatten('C')
    arr = ''.join(ch for ch in arr)
    arr = arr.replace('~', '')
    return arr


def get_original_positions(original):
    positions = []
    org = []
    for i in range(len(original)):
        org.append((original[i], i))
    mov = sorted(org, key=lambda x: x[0])
    for i in org:
        index = 0
        for j in mov:
            if i[1] != j[1]:
                index += 1
            else:
                positions.append(index)
                index = 0
    return positions


def encrypt(keyword, text):
    text = str(text).upper().replace(' ', '')
    words_in_keyword = len(str(keyword).split())
    first_round = round_of_ubich(keyword, text)
    null_letters = ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(words_in_keyword))
    first_round = first_round + null_letters
    second_round = round_of_ubich(keyword, first_round)
    print(f'Encrypted message: {second_round}')
    return second_round


def decrypt(keyword, text):
    text = str(text).upper()
    words_in_keyword = len(str(keyword).split())
    first_round = round_of_ubich_decrypt(keyword, text)
    first_round = first_round[:len(text)-words_in_keyword]
    print(f'Krok 4: \n{first_round}')
    second_round = round_of_ubich_decrypt(keyword, first_round)
    return second_round
