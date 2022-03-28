from stest import stest
from random import randint
from time import time
from math import gcd
from collections import deque
from copy import copy

path_to_save = "lab4-bbs-rsa/test_1mln_1.txt"
p, q = 11, 23
bits_to_generate = 10**6


def bbs(p, q, k):  # Blum Blum Shub Random Bit generator. Input two large primes 3mod4 and the number of bits in the output

    t = time()				      # start the clock
    rngs = deque()          # store the rngs for testing

    n = p*q
    # phi is the number of elements in the multiplicative group of Z/nZ
    phi = (p-1) * (q-1)

    x_0 = (p-1)					    # x_0 is the seed
    while (gcd(x_0, phi) != 1):  # this block of code chooses x_0 so that gcd(x_0,phi)=1
        x_0 = randint(2, phi-1)

    z = 0					            # initialize z (the bit component)

    for _ in range(k):      # generate sequence of k integers
        x_0 = (x_0*x_0) % n

        if (x_0 > n / 2):
            x_0 = n - x_0
        z = x_0 % 2
        rngs.append(z)

    t = time()-t
    print('--------')
    print(f'{k} bits generated with BBS')
    print(f'Generating time: {t}')

    return rngs


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
        deq = bbs(p, q, bits_to_generate)
        print(deq)
        stest(copy(deq))
        f.write("".join(str(i) for i in deq))

    print("Succes!")
