import stest

path_to_key = "lab4-bbs-rsa/test_20k_1.txt"
path_to_text = "lab4-bbs-rsa/text.txt"


def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def frombits(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def xor(a, b):
    return int(bool(a) ^ bool(b))


def encrypt(bits, key):
    xored = [xor(a, b) for (a, b) in zip(bits, key)]
    return xored


def decrypt(bits, key):
    xored = [xor(a, b) for (a, b) in zip(bits, key)]
    return xored


if __name__ == "__main__":
    with open(path_to_key, "r") as f_key:
        with open(path_to_text, "r") as f_text:
            key = f_key.read()
            text = tobits(f_text.read())
            encrypted = encrypt(text, key)
            decrypted = decrypt(encrypted, key)
            encrypted_str = ''.join([str(i) for i in encrypted])
            stest.bits_test(encrypted_str)
            stest.series_test(encrypted_str)
            stest.long_series_test(encrypted_str)
            stest.poker_test(encrypted_str)

            print(frombits(decrypted))
