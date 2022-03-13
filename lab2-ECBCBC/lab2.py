from Crypto.Cipher import AES
from padding import pad, unpad, xor
'''Alphabet is utf-8'''

invo = '''Litwo, Ojczyzno moja! ty jesteś jak zdrowie;
Ile cię trzeba cenić, ten tylko się dowie,
Kto cię stracił. Dziś piękność twą w całej ozdobie
Widzę i opisuję, bo tęsknię po tobie.

Panno święta, co Jasnej bronisz Częstochowy
I w Ostrej świecisz Bramie! Ty, co gród zamkowy
Nowogródzki ochraniasz z jego wiernym ludem!
Jak mnie dziecko do zdrowia powróciłaś cudem
(— Gdy od płaczącej matki, pod Twoją opiekę
Ofiarowany martwą podniosłem powiekę;
I zaraz mogłem pieszo, do Twych świątyń progu
Iść za wrócone życie podziękować Bogu —)
Tak nas powrócisz cudem na Ojczyzny łono!...
Tymczasem, przenoś moją duszę utęsknioną
Do tych pagórków leśnych, do tych łąk zielonych,
Szeroko nad błękitnym Niemnem rozciągnionych;
Do tych pól malowanych zbożem rozmaitem,
Wyzłacanych pszenicą, posrebrzanych żytem;
Gdzie bursztynowy świerzop, gryka jak śnieg biała,
Gdzie panieńskim rumieńcem dzięcielina pała,
A wszystko przepasane jakby wstęgą, miedzą
Zieloną, na niej zrzadka ciche grusze siedzą.'''

key = b'Dzis jest piekny dzien!'
message = bytes(invo, 'utf-8')


def aes_ecb_encrypt(message, key, iv):
    obj = AES.new(key, AES.MODE_ECB)
    return obj.encrypt(message)


def aes_ecb_decrypt(message, key, iv):
    obj = AES.new(key, AES.MODE_ECB)
    return obj.decrypt(message)


def aes_cbc_encrypt(message, key, iv=b'\x00' * 16):
    prev_chunk = iv
    encrypted = []

    for i in range(0, len(message), 16):
        chunk = message[i: i + 16]
        encrypted_block = aes_ecb_encrypt(xor(chunk, prev_chunk), key, iv)
        encrypted += encrypted_block
        prev_chunk = encrypted_block

    return bytes(encrypted)


def aes_cbc_decrypt(message, key, iv=b'\x00' * 16):
    prev_chunk = iv

    decrypted = []

    for i in range(0, len(message), 16):
        chunk = message[i: i + 16]
        decrypted += xor(aes_ecb_decrypt(chunk, key, iv), prev_chunk)
        prev_chunk = chunk

    return bytes(decrypted)


def aes_ofb_encrypt(message, key, iv=b'\x00' * 16):
    prev_chunk = iv
    encrypted = []

    for i in range(0, len(message), 16):
        encrypted_block = aes_ecb_encrypt(prev_chunk, key, iv)
        chunk = message[i: i + 16]
        ciphertext_block = xor(chunk, encrypted_block)
        encrypted += ciphertext_block
        prev_chunk = encrypted_block

    return bytes(encrypted)


def aes_ofb_decrypt(message, key, iv=b'\x00' * 16):
    prev_chunk = iv
    decrypted = []

    for i in range(0, len(message), 16):
        encrypted_block = aes_ecb_encrypt(prev_chunk, key, iv)
        chunk = message[i: i + 16]
        plaintext_block = xor(encrypted_block, chunk)
        decrypted += plaintext_block
        prev_chunk = encrypted_block

    return bytes(decrypted)


def print_blocks(message):
    hexed = message.hex()
    for i in range(0, len(message), 64):
        print(
            f'{hexed[i: i + 16]}\t{hexed[i+16: i + 32]}\t{hexed[i+32: i + 48]}\t{hexed[i+48: i + 64]}', end='')
        print()
        if i % 256 == 0 and i != 0:
            print()


def test_encryption(message, key, iv):
    # ECB MODE
    encrypted_ecb = aes_ecb_encrypt(message, key, iv=iv)
    print(
        f'MESSAGE ENCRYPTED IN ECB MODE \nKey: {key}\nInitialize vector: {iv}:')
    print_blocks(encrypted_ecb)

    print(
        f'MESSAGE DECRYPTED IN ECB MODE \nKey: {key}\nInitialize vector: {iv}:')
    decrypted_ecb = aes_ecb_decrypt(encrypted_ecb, key, iv=iv)
    print_blocks(decrypted_ecb)
    # CBC MODE
    encrypted_cbc = aes_cbc_encrypt(message, key, iv=iv)
    print(
        f'MESSAGE ENCRYPTED IN CBC MODE \nKey: {key}\nInitialize vector: {iv}:')
    print_blocks(encrypted_cbc)

    print(
        f'MESSAGE DECRYPTED IN CBC MODE \nKey: {key}\nInitialize vector: {iv}:')
    decrypted_cbc = aes_cbc_decrypt(encrypted_cbc, key, iv=iv)
    print_blocks(decrypted_cbc)
    # OFB MODE
    encrypted_ofb = aes_ofb_encrypt(message, key, iv=iv)
    print(
        f'MESSAGE ENCRYPTED IN OFB MODE \nKey: {key}\nInitialize vector: {iv}:')
    print_blocks(encrypted_ofb)

    print(
        f'MESSAGE DECRYPTED IN OFB MODE \nKey: {key}\nInitialize vector: {iv}:')
    decrypted_ofb = aes_ofb_decrypt(encrypted_ofb, key, iv=iv)
    print_blocks(decrypted_ofb)

    print("Original plaintext")
    print(unpad(decrypted_ofb, 16).decode('utf-8'))


if __name__ == '__main__':
    padded_key = pad(key, 16)
    padded_message = pad(message, 16)
    iv = b'0123456789ABCDEF'
    test_encryption(padded_message, padded_key, iv)
