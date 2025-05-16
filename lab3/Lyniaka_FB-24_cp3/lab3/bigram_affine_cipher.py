from affine_cipher import inverse
from bigram_alphabet import BigramAlphabet


def gcd(m, n):
    if m == 0 and n == 0:
        return 0

    if n == 0:
        return m

    while m != 0:
        n = n % m
        n, m = m, n
    return n


def congruence_solver(a, b, m):
    """Solves ax = b mod m congruence"""
    solutions = []
    d = gcd(a, m)
    if d != 1:
        if d == 0 or b % d != 0:
            return solutions

        a //= d
        b //= d
        m //= d
    a1 = inverse(a, m)
    x = (a1 * b) % m
    if d == 1:
        solutions.append(x)
    else:
        solutions = [x + k * m for k in range(d)]
    return solutions


def get_affine_keys_from_congruence(y1, y2, x1, x2, m):
    """Find a from (y1 - y2) = a(x1 - x2) (mod m)"""
    a_inversed_list = congruence_solver((y1 - y2 + m) % m, (x1 - x2 + m) % m, m)
    a_b_list = list()
    for a_inversed in a_inversed_list:
        a = inverse(a_inversed, m)
        if a is None:
            continue

        b = (y1 + m - a * x1) % m
        a_b_list.append((a, b))
    return a_b_list


class BigramAffineCipher:

    def __init__(self, a, b, bigram_alphabet: BigramAlphabet):
        self._a = a
        self._b = b
        self._bigram_alphabet = bigram_alphabet
        self._m = self._bigram_alphabet.m2
        self._a_inversed = inverse(self._a, self._m)
        if self._a_inversed is None:
            raise ValueError(f"Parameter a({self._a}) is not coprime to m({self._m})")

    def cipher(self, bigrams_string):
        numbers_list = [(self._a * x + self._b) % self._m
                        for x in self._bigram_alphabet.get_numbers_list(bigrams_string)]
        return self._bigram_alphabet.get_bigrams_list(numbers_list)

    def decipher(self, ciphered_bigrams_string):
        numbers_list = [self._a_inversed * (x + self._m - self._b) % self._m
                        for x in self._bigram_alphabet.get_numbers_list(ciphered_bigrams_string)]
        return self._bigram_alphabet.get_bigrams_list(numbers_list)
