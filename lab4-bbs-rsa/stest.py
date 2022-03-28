from math import floor


def stest(rngs):

    size = len(rngs)                # here rngs should be a deque type

    freq = 0                        # here we count the number of 1s
    switch = 0                      # here we count the number of bit switches

    # poker test
    # each entry correspond to the binary representation
    poker = [0]*32
    # for example, poker[2] count the number of bit sequences
    # of the form 00010

    switchtemp = 0                    # temp variable for switch

    numof5sequence = floor(size/5)
    for _ in range(numof5sequence):  # we consider disjoint 5 bit sequences

        index = 0             # this will tell us what kind of bit sequence this is

        for i in range(5):            # we consider disjoint 5 bit sequences
            z = rngs.popleft()
            freq += z                   # here we count 1s
            switch += z ^ switchtemp       # here we count switches-"^" is xor
            switchtemp = z

            # here we convert the 5 bit sequence into
            index += pow(2, 4-i)*z
            # the index for the poker array
        poker[index] += 1


# here we compute chi square of poker test
    chi2 = 0
    expected = float(numof5sequence)/32
    for i in poker:
        chi2 += pow(i-expected, 2)/expected
# we test multiples of 5 bits so we set tsize to that
    tsize = (size//5)*5

    print(f'Frequency of 1s: {float(freq)/tsize}')
    print(f'Frequency of switches: {float(switch)/tsize}')
    print(f'Chi Square of Poker test: {chi2}')

    return [float(freq)/tsize, float(switch)/tsize, chi2]
