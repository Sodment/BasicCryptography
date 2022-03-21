from Crypto.Cipher import AES
from padding import pad, unpad, xor
import timeit
invo_short = ''
invo_medium = ''
invo_long = ''
key = b'Dzis jest piekny dzien!'

with open('lab2-ECBCBC/test_1.txt', mode='r', encoding='utf-8') as f:
    invo_short = f.read()
with open('lab2-ECBCBC/test_2.txt', mode='r', encoding='utf-8') as f:
    invo_medium = f.read()
with open('lab2-ECBCBC/test_3.txt', mode='r', encoding='utf-8') as f:
    invo_long = f.read()

message_short = bytes(invo_short, 'utf-8')
message_medium = bytes(invo_medium, 'utf-8')
message_long = bytes(invo_long, 'utf-8')


def time_test(function):
    def wrapper_time_test(*args, **kwargs):
        start_time = timeit.default_timer()
        result = function(*args, **kwargs)
        end_time = timeit.default_timer()
        return (end_time-start_time)*(10**6), result
    return wrapper_time_test


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


@time_test
def aes_encrypt(message, key, mode=AES.MODE_ECB, *args):
    obj = AES.new(key, mode, *args)
    return obj.encrypt(message)


@time_test
def aes_decrypt(message, key, mode=AES.MODE_ECB, *args):
    obj = AES.new(key, mode, *args)
    return obj.decrypt(message)


def test_times(message, key, iv):
    modes = [AES.MODE_ECB, AES.MODE_CBC,
             AES.MODE_CFB, AES.MODE_OFB]
    encrypted = []
    encrypted.append(aes_encrypt(message, key, modes[0]))
    encrypted.append(aes_encrypt(message, key, modes[1], iv))
    encrypted.append(aes_encrypt(message, key, modes[2], iv))
    encrypted.append(aes_encrypt(message, key, modes[3], iv))

    decrypted = []
    for i in encrypted:
        decrypted.append(aes_decrypt(message, key, modes[3], iv))

    encryption_times = [x[0] for x in encrypted]
    decryption_times = [x[0] for x in decrypted]
    return encryption_times, decryption_times


def delete_block(message):
    if len(message) <= 32:
        return message
    else:
        message = message[0:16] + message[32:]
        return message


def test_block_deletion(message, key, iv):
    ecb = delete_block(aes_ecb_encrypt(message, key, iv=iv))
    cbc = delete_block(aes_cbc_encrypt(message, key, iv=iv))
    ofb = delete_block(aes_ofb_encrypt(message, key, iv=iv))

    ecb_decrypted = aes_ecb_decrypt(ecb, key, iv=iv)
    print(f"ECB decrypted with block deletion:")
    print_blocks(ecb_decrypted)
    print("Original plaintext")
    print(unpad(ecb_decrypted, 16).decode('utf-8'))
    cbc_decrypted = aes_cbc_decrypt(cbc, key, iv=iv)
    print(f"CBC decrypted with block deletion:")
    print_blocks(cbc_decrypted)
    print("Original plaintext")
    try:
        print(unpad(cbc_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    ofb_decrypted = aes_ofb_decrypt(ofb, key, iv=iv)
    print(f"OFB decrypted with block deletion:")
    print_blocks(ofb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ofb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")


def double_block(message):
    if len(message) <= 32:
        return message
    else:
        message = message[0:16] + message[16:32] + \
            message[16:32] + message[32:]
        return message


def test_block_double(message, key, iv):
    ecb = double_block(aes_ecb_encrypt(message, key, iv=iv))
    cbc = double_block(aes_cbc_encrypt(message, key, iv=iv))
    ofb = double_block(aes_ofb_encrypt(message, key, iv=iv))

    ecb_decrypted = aes_ecb_decrypt(ecb, key, iv=iv)
    print(f"ECB decrypted with block doubling:")
    print_blocks(ecb_decrypted)
    print("Original plaintext")
    print(unpad(ecb_decrypted, 16).decode('utf-8'))
    cbc_decrypted = aes_cbc_decrypt(cbc, key, iv=iv)
    print(f"CBC decrypted with block doubling:")
    print_blocks(cbc_decrypted)
    print("Original plaintext")
    try:
        print(unpad(cbc_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    ofb_decrypted = aes_ofb_decrypt(ofb, key, iv=iv)
    print(f"OFB decrypted with block doubling:")
    print_blocks(ofb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ofb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")


def exchange_block(message):
    if len(message) <= 64:
        return message
    else:
        message = message[0:16] + message[32:48] + \
            message[16:32] + message[48:]
        return message


def test_block_exchange(message, key, iv):
    ecb = exchange_block(aes_ecb_encrypt(message, key, iv=iv))
    cbc = exchange_block(aes_cbc_encrypt(message, key, iv=iv))
    ofb = exchange_block(aes_ofb_encrypt(message, key, iv=iv))

    ecb_decrypted = aes_ecb_decrypt(ecb, key, iv=iv)
    print(f"ECB decrypted with block exchanging:")
    print_blocks(ecb_decrypted)
    print("Original plaintext")
    print(unpad(ecb_decrypted, 16).decode('utf-8'))
    cbc_decrypted = aes_cbc_decrypt(cbc, key, iv=iv)
    print(f"CBC decrypted with block exchanging:")
    print_blocks(cbc_decrypted)
    print("Original plaintext")
    try:
        print(unpad(cbc_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    ofb_decrypted = aes_ofb_decrypt(ofb, key, iv=iv)
    print(f"OFB decrypted with block exchanging:")
    print_blocks(ofb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ofb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")


def add_new_block(message, block):
    if len(message) <= 32:
        return message
    else:
        message = message + block
        return message


def test_block_addition(message, key, iv):
    block = aes_ecb_encrypt(pad(b'Dodatkowy blok', 16), key, iv=iv)
    ecb = add_new_block(aes_ecb_encrypt(message, key, iv=iv), block)
    cbc = add_new_block(aes_cbc_encrypt(message, key, iv=iv), block)
    ofb = add_new_block(aes_ofb_encrypt(message, key, iv=iv), block)

    ecb_decrypted = aes_ecb_decrypt(ecb, key, iv=iv)
    print(f"ECB decrypted with block addition:")
    print_blocks(ecb_decrypted)
    print("Original plaintext")
    print(unpad(ecb_decrypted, 16).decode('utf-8'))
    cbc_decrypted = aes_cbc_decrypt(cbc, key, iv=iv)
    print(f"CBC decrypted with block addition:")
    print_blocks(cbc_decrypted)
    print("Original plaintext")
    try:
        print(unpad(cbc_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    ofb_decrypted = aes_ofb_decrypt(ofb, key, iv=iv)
    print(f"OFB decrypted with block addition:")
    print_blocks(ofb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ofb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")


def change_one_byte(message):
    if len(message) <= 32:
        return message
    else:
        message = bytearray(message)
        message[16] += 1
        return bytes(message)


def test_block_change_one_byte(message, key, iv):
    ecb = change_one_byte(aes_ecb_encrypt(message, key, iv=iv))
    cbc = change_one_byte(aes_cbc_encrypt(message, key, iv=iv))
    ofb = change_one_byte(aes_ofb_encrypt(message, key, iv=iv))

    ecb_decrypted = aes_ecb_decrypt(ecb, key, iv=iv)
    print(f"ECB decrypted with block with changing one byte:")
    print_blocks(ecb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ecb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    cbc_decrypted = aes_cbc_decrypt(cbc, key, iv=iv)
    print(f"CBC decrypted with block changing one byte:")
    print_blocks(cbc_decrypted)
    print("Original plaintext")
    try:
        print(unpad(cbc_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    ofb_decrypted = aes_ofb_decrypt(ofb, key, iv=iv)
    print(f"OFB decrypted with block changing one byte:")
    print_blocks(ofb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ofb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")


def swap_bytes(message):
    if len(message) <= 32:
        return message
    else:
        message = bytearray(message)
        message[17], message[18] = message[18], message[17]
        return bytes(message)


def test_block_swap_bytes(message, key, iv):
    ecb = swap_bytes(aes_ecb_encrypt(message, key, iv=iv))
    cbc = swap_bytes(aes_cbc_encrypt(message, key, iv=iv))
    ofb = swap_bytes(aes_ofb_encrypt(message, key, iv=iv))

    ecb_decrypted = aes_ecb_decrypt(ecb, key, iv=iv)
    print(f"ECB decrypted with block with exchanging one byte:")
    print_blocks(ecb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ecb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    cbc_decrypted = aes_cbc_decrypt(cbc, key, iv=iv)
    print(f"CBC decrypted with block exchanging one byte:")
    print_blocks(cbc_decrypted)
    print("Original plaintext")
    try:
        print(unpad(cbc_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    ofb_decrypted = aes_ofb_decrypt(ofb, key, iv=iv)
    print(f"OFB decrypted with block exchanging one byte:")
    print_blocks(ofb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ofb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")


def delete_one_byte(message):
    if len(message) <= 32:
        return message
    else:
        message = bytearray(message)
        del message[22]
        return bytes(message)


def test_block_delete_bytes(message, key, iv):
    ecb = delete_one_byte(aes_ecb_encrypt(message, key, iv=iv))
    cbc = delete_one_byte(aes_cbc_encrypt(message, key, iv=iv))
    ofb = delete_one_byte(aes_ofb_encrypt(message, key, iv=iv))

    ecb_decrypted = aes_ecb_decrypt(ecb, key, iv=iv)
    print(f"ECB decrypted with block with deleting one byte:")
    print_blocks(ecb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ecb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    cbc_decrypted = aes_cbc_decrypt(cbc, key, iv=iv)
    print(f"CBC decrypted with block deleting one byte:")
    print_blocks(cbc_decrypted)
    print("Original plaintext")
    try:
        print(unpad(cbc_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")
    ofb_decrypted = aes_ofb_decrypt(ofb, key, iv=iv)
    print(f"OFB decrypted with block deleting one byte:")
    print_blocks(ofb_decrypted)
    print("Original plaintext")
    try:
        print(unpad(ofb_decrypted, 16).decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        print("Message unreadable!")


if __name__ == '__main__':
    padded_key = pad(key, 16)
    padded_message = pad(message_short, 16)
    iv = b'0123456789ABCDEF'
    test_encryption(padded_message, padded_key, iv)
    # MSG Short
    print(test_times(padded_message, padded_key, iv))

    # MSG Medium
    padded_message = pad(message_medium, 16)
    print(test_times(padded_message, padded_key, iv))

    # MSG Long
    padded_message = pad(message_long, 16)
    print(test_times(padded_message, padded_key, iv))

    padded_message = pad(message_medium, 16)
    test_block_deletion(padded_message, padded_key, iv)
    test_block_double(padded_message, padded_key, iv)
    test_block_exchange(padded_message, padded_key, iv)
    test_block_addition(padded_message, padded_key, iv)
    test_block_change_one_byte(padded_message, padded_key, iv)
    test_block_swap_bytes(padded_message, padded_key, iv)
    test_block_delete_bytes(padded_message, padded_key, iv)
