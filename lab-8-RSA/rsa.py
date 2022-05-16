from math import sqrt, gcd, floor
from random import randint


def co_prime(n):
    coprimes = []
    for i in range(n):
        if gcd(i, n) == 1:
            coprimes.append(i)
    i = randint(0, len(coprimes)-1)
    return coprimes[i]


def gen_prime(digits: int):
    lower = 10**(digits-1)
    upper = 10**digits
    primes = []
    for num in range(lower, upper):
        if num > 1:
            for i in range(2, floor(sqrt(num))):
                if (num % i) == 0:
                    break
            else:
                primes.append(num)
    i = randint(0, len(primes)-1)
    return primes[i]


def gen_d(e, fi):
    for d in range(fi):
        if (e * d - 1) % fi == 0:
            return d


def rsa():
    p, q = gen_prime(4), gen_prime(4)
    n = p * q
    fi = (p-1)*(q-1)
    e = co_prime(fi)
    d = gen_d(e, fi)
    print(f"P: {p} Q: {q}")
    print(f"Fi: {fi}")
    print(f"Public key e: {e} n: {n}")
    print(f"Private key d: {d} n: {n}")

    return ((e, n), (d, n))


def simple_math(m: int, power: int, modulo: int):
    return m**power % modulo


def encrypt(message, key: tuple):
    encrypted = []
    for ch in message:
        encrypted.append(simple_math(ord(ch), key[0], key[1]))
    return encrypted


def decrypt(message, key: tuple):
    decrypted = []
    for ch in message:
        decrypted.append(chr(simple_math(ch, key[0], key[1])))
    return decrypted


def simple_encrypt(message, key: tuple):
    print("Im encrypting!")
    encrypted = 0
    for ch in message:
        encrypted += ord(ch)
    return simple_math(encrypted, key[0], key[1])


def simple_decrypt(message, key: tuple):
    decrypted = simple_math(message, key[0], key[1])
    return decrypted


if __name__ == "__main__":
    public, private = rsa()
    encrypted = encrypt(
        'Ta wiadomosc ma rowne piecdziesiat znakow raz dwa!', public)
    print(encrypted)
    print(decrypt(encrypted, private))
