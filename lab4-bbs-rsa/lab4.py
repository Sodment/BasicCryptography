import stest
from random import randint, getrandbits
from time import time
from math import gcd
from collections import deque
from copy import copy

path_to_save = "lab4-bbs-rsa/test_1mln_1.txt"
p, q = 11, 23
bits_to_generate = 1000000


def decompose(n):
    exponentOfTwo = 0

    while n % 2 == 0:
        n = n//2
        exponentOfTwo += 1

    return exponentOfTwo, n


def isWitness(possibleWitness, p, exponent, remainder):
    possibleWitness = pow(possibleWitness, remainder, p)

    if possibleWitness == 1 or possibleWitness == p - 1:
        return False

    for _ in range(exponent):
        possibleWitness = pow(possibleWitness, 2, p)

        if possibleWitness == p - 1:
            return False

    return True


def probablyPrime(p, accuracy=100):
    if p == 2 or p == 3:
        return True
    if p < 2:
        return False

    exponent, remainder = decompose(p - 1)

    for _ in range(accuracy):
        possibleWitness = randint(2, p - 2)
        if isWitness(possibleWitness, p, exponent, remainder):
            return False

    return True


def goodPrime(p):
    return p % 4 == 3 and probablyPrime(p, accuracy=100)


def findGoodPrime(numBits=128):
    candidate = 1
    while not goodPrime(candidate):
        candidate = getrandbits(numBits)
    return candidate


def makeModulus():
    return findGoodPrime() * findGoodPrime()


def parity(n):
    return sum(int(x) for x in bin(n)[2:]) % 2


class BlumBlumShub(object):
    def __init__(self, seed=None):
        self.modulus = makeModulus()
        self.state = seed if seed is not None else randint(2, self.modulus - 1)
        self.state = self.state % self.modulus

    def seed(self, seed):
        self.state = seed

    def bitstream(self):
        while True:
            yield parity(self.state)
            self.state = pow(self.state, 2, self.modulus)

    def bits(self, n=20):
        outputBits = ''
        for bit in self.bitstream():
            outputBits += str(bit)
            if len(outputBits) == n:
                break

        return outputBits


def rsa(p, q, k):

    t = time()              # we start the clock here
    rngs = deque()          # store the rngs for testing

    n = p*q
    phi = (p-1) * (q-1)

    e = (p-1)               # this block of code choses e so that gcd(e,phi)=1
    while (gcd(e, phi) != 1):
        e = randint(2, phi-1)

    x_0 = (p-1)             # this block of code choses x_0 so that gcd(x_0,phi)=1
    while (gcd(e, phi) != 1):
        x_0 = randint(2, phi-1)

    for _ in range(k):      # here we generate k values
        x_0 = pow(x_0, e, n)
        rngs.append(x_0 % 2)

    t = time()-t
    print('--------')
    print('{0} bits generated with RSA'.format(k))
    print('Generating time: {0}'.format(t))

    sarray = stest(rngs)
    sarray.insert(0, t)

    return rngs


if __name__ == '__main__':
    with open(path_to_save, "w") as f:
        generator = BlumBlumShub()
        res = generator.bits(bits_to_generate)
        f.write(res)
        stest.bits_test(res)
        stest.series_test(res)
        stest.long_series_test(res)
        stest.poker_test(res)
