import string
from scipy.special import comb
from scipy.stats import chi2
import numpy as np
from collections import Counter
import math
import textwrap
import pandas as pd


def bits_test(s: list):
    ones = s.count('1')
    if 9725 < ones < 10275:
        print(f"BITS TEST: PASSED, Value of test {ones}")
    else:
        print(f"BITS TEST: FAILED, Value of test {ones}")


def series_test_2(s: string):
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
             'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(1, 13):
        series_1 = '0' + (i * '1') + '0'
        series_0 = '1' + (i * '0') + '1'
        s = s.replace(series_1, alpha[i])
        s = s.replace(series_0, alpha[13+i])

    print(s)
    print(s.count('b'))


def series_test(s: string):
    result_ones = []
    result_zeros = []
    for i in range(1, 26):
        result_ones.append(s.count(i * '1'))
        result_zeros.append(s.count(i * '0'))
    result_ones[6] = sum(result_ones[6:])
    result_ones = result_ones[:6]
    result_zeros[6] = sum(result_zeros[6:])
    result_zeros = result_zeros[:6]

    for i in range(6):
        result_ones[i] = result_ones[i] - sum(result_ones[i+1:])
        result_zeros[i] = result_zeros[i] - sum(result_zeros[i+1:])

    intervals = [(2315, 2685), (1114, 1386), (527, 723),
                 (240, 384), (103, 209), (103, 209)]
    result = 1
    for i in range(6):
        if not(intervals[i][0] < result_ones[i] < intervals[i][1]):
            result = 0
    if result == 1:
        print(
            f"SERIES TEST: PASSED, Value of test 1:{result_ones}, 0:{result_zeros}")
    else:
        print(
            f"SERIES TEST: PASSED, Value of test 1:{result_ones}, 0:{result_zeros}")


def long_series_test(s: list):
    ones = s.count(26*'1')
    zeros = s.count(26*'0')

    if zeros == 0 and ones == 0:
        print(f"LONG SERIES TEST: PASSED, Value of test 1:{ones}, 0:{zeros}")
    else:
        print(f"LONG SERIES TEST: FAILED, Value of test 1:{ones}, 0:{zeros}")


def poker_test(s: string):
    splitted = textwrap.wrap(s, 4)
    bits = {
        '0000': 0,
        '0001': 0,
        '0010': 0,
        '0011': 0,
        '0100': 0,
        '0101': 0,
        '0110': 0,
        '0111': 0,
        '1000': 0,
        '1001': 0,
        '1010': 0,
        '1011': 0,
        '1100': 0,
        '1101': 0,
        '1110': 0,
        '1111': 0,
    }
    for hex_number in splitted:
        bits[hex_number] += 1

    result = []
    for val in bits:
        x = bits[val]**2
        result.append(x)
    result = sum(result)
    result = 16/5000 * result - 5000
    if 2.16 < result < 46.17:
        print(f"POKER TEST: PASSED, Value of test {result}")
    else:
        print(f"POKER TEST: FAILED, Value of test {result}")


def poker_test_2(s, m):
    X2theoretical = [3.84, 5.99, 7.81, 9.48, 11.07, 12.59, 14.06]
    k = len(s)//m
    l = list(np.arange(0, k))
    s1 = s
    for i in range(0, k):
        while len(s1) > 0:
            l[i] = s1[:m]
            s1 = s1[m:]
            break
    n = l
    for j, i in enumerate(l):
        try:
            n[j] = Counter(i)['1']
        except:
            n[j] = Counter(i)['0']

    n.sort()
    niDict = dict(Counter(n))
    # we create a dummy dictionary with keys
    k = [i for i in range(0, m+1)]
    dummydict = dict(zip(k, [0]*len(k)))

    def check_existance(i, collection: iter):
        return i in collection
    if dummydict.keys() == niDict.keys():
        print('ok')
    else:
        for i in dummydict.keys():
            if check_existance(i, niDict.keys()) == False:
                niDict[i] = 0
    b = []

    for i in niDict.keys():

        numerator = math.pow(niDict[i] - comb(m, i)*len(s)/((2**m)*m), 2)
        denominator = comb(m, i)*len(s)/((2**m)*m)
        S = numerator / denominator
        b.append(S)

    X2 = sum(b)
    if X2 < chi2.isf(0.05, m-1):
        print('POKER TEST: PASSED')
    else:
        print('POKER TEST:')
    return X2
