from itertools import permutations
from math import gcd


alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
m = len(alphabet)  
m2 = m**2  


def bigram_to_number(bigram, alphabet):
    return alphabet.index(bigram[0]) * m + alphabet.index(bigram[1])

def modular_inverse(a, mod):
    a = a % mod
    for x in range(1, mod):
        if (a * x) % mod == 1:
            return x
    return None

language_bigrams = ['ст', 'но', 'то', 'на', 'ен']  
cipher_bigrams = ['вв', 'эл', 'вм', 'хм', 'ух']    


lang_numbers = [bigram_to_number(bigram, alphabet) for bigram in language_bigrams]
cipher_numbers = [bigram_to_number(bigram, alphabet) for bigram in cipher_bigrams]

pairs = list(permutations(zip(lang_numbers, cipher_numbers), 2))  

candidates = []
for pair in pairs:
    (X1, Y1), (X2, Y2) = pair


    delta_x = (X1 - X2) % m2
    delta_y = (Y1 - Y2) % m2


    if gcd(delta_x, m2) == 1:  
        a = (delta_y * modular_inverse(delta_x, m2)) % m2
        b = (Y1 - a * X1) % m2
        candidates.append((a, b))

print("Key candidates (a, b):")
for candidate in candidates:
    print(candidate)
