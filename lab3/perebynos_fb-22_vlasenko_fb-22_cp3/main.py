#!/bin/python
from typing import Callable
from itertools import permutations
import subprograms as sp
import pprint

TESTDATA = "./data/V2"
VARDATA = "./data/02.txt"
EXITMSG = "No integer solutions exist. Skipping...\n"
MOSTFREQBIGRAMS = ["то", "на", "ст", "но", "ен"]
BANNEDBIGRAMS = ["аь", "оь", "яь", "юь", "еь", "ыь"]
MODULUS = len(sp.ALPHABET)**2

def main():
    test_data = sp.readText(VARDATA)

    freqs = sp.calculateFrequenciesFirst(test_data, 10)
    pprint.pprint(freqs)

    mf = []
    for i in freqs:
        mf.append(i[0])

    x1 = sp.bigramToNumber(MOSTFREQBIGRAMS[0])
    x2 = sp.bigramToNumber(MOSTFREQBIGRAMS[1])
    x = x1 - x2
    gcd, xInv = sp.gcdEuclideanExtended2(x, MODULUS)
    if gcd != 1:
        print(f"GCD of x1-x2 and {MODULUS} != 1: {gcd}")

    for bigram in permutations(mf, 2):
        if bigram[0] == bigram[1]:
            continue

        # y = a*x + b mod m
        # y1 = a*x1 + b mod m
        # y2 = a*x2 + b mod m

        # (y1 - y2) = a*(x1 - x2) mod m
        # a = (y1 - y2) * (x1 - x2)^-1 mod m
        # b = y1-a*x1 mod m
        y1 = sp.bigramToNumber(bigram[0])
        y2 = sp.bigramToNumber(bigram[1])
        a = ((y1 - y2) * xInv) % MODULUS
        b = (y1 - a * x1) % MODULUS

        # x = (y-b)*(a**(-1)) mod m
        gcd, _ = sp.gcdEuclideanExtended2(a, MODULUS)
        if gcd != 1:
            continue

        decryptor = sp.AfineDecryptor(a, b, MODULUS)
        dec = decryptor.decrypt(test_data)
        
        for i in BANNEDBIGRAMS:
            if dec.find(i) != -1:
                print(f"Found banned bigram: {i} for a = {a}, b = {b}")
                break
        else:
            print(f"May be key a = {a}, b = {b}")
            print(f"Text: {dec[:100]}")
            with open("./data/dec.txt", "w") as f:
                f.write(dec)
            return


if __name__ == "__main__":
    main()
