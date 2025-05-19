import re
from collections import Counter
from collections import defaultdict
import itertools
alh =  "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alh)
m2 = m*m


def extendedev(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extendedev(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y


def mod(x, mod):
    x %= mod
    if x < 0:
        return x + mod
    return x


def modin(a, m):
    g, x, _ = extendedev(a, m)
    if g != 1:
        return -1  
    else:
        return x % m  


def solve_linear_congruence(a, b, m):
    g, _, _ = extendedev(a, m)
    solutions = []

    if b % g != 0:
        return solutions  

    a //= g
    b //= g
    m //= g
    inv = modin(a, m)
    if inv == -1:
        return solutions
    x0 = (inv * b) % m
    for i in range(g):
        solutions.append((x0 + i * m) % m)
    return solutions


def read_ciphertext(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().replace("\n", "")


def get_bigrams(text):
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 2)]
    return Counter(bigrams)


def decrypt_text(ciphertext, inv_a, b):
    decrypted_text = ""
    for i in range(0, len(ciphertext)-1, 2):  
        y = alh.index(ciphertext[i])*m +  alh.index(ciphertext[i+1])
        x = (inv_a*(y-b))%m2
        decrypted_text += alh[x//m] + alh[x%m]
    return decrypted_text


def generate_candidates(common_bigrams, ciphertext_bigrams):
    top_ciphertext_bigrams = [key for key, _ in sorted(ciphertext_bigrams.items(), key=lambda x: x[1], reverse=True)[:5]]
    candidates = set()
    pairs = set()
    for common_bigram in common_bigrams:
        for ciphertext_bigram in top_ciphertext_bigrams:
            pairs.add(((alh.index(common_bigram[0])*m + alh.index(common_bigram[1]))%m2, (alh.index(ciphertext_bigram[0])*m + alh.index(ciphertext_bigram[1]))%m2))
    for (x1, y1), (x2, y2) in itertools.combinations(pairs, 2):
        all_a = solve_linear_congruence(mod(x1 - x2, m2), mod(y1 - y2, m2), m2)
        for a in all_a:
            ain = modin(a, m2)
            if ain:
                b = (y1 - a*x1)%m2
                candidates.add((a, ain, b))
    print(len(candidates))
    return candidates


def Index_С(text):
    n = len(text)
    if n <= 1:
        return 0
    
    frequencies = Counter(text)
    ic = 0
    for freq in frequencies.values():
        ic += freq * (freq - 1)
    
    return ic / (n * (n - 1))


def is_russian(text):
    if Index_С(text) < 0.045:
        return False
    freqs = Counter(text)
   
    common_letters = ["о", "а", "е"]
    uncommon_letters = ["ф", "щ", "ь"]

    freq_of_common_letters = sum(freqs[letter] for letter in common_letters if letter in freqs) / len(text)
    if freq_of_common_letters < 0.2:
        return False

    freq_of_uncommon_letters = sum(freqs[letter] for letter in uncommon_letters if letter in freqs) / len(text)
    if freq_of_uncommon_letters > 0.05:
        return False

    popular_trigrams = {"про", "ста", "ено", "сна", "ног"}
    trigrams = defaultdict(int)

    for i in range(len(text) - 2):
        trigram = text[i:i + 3]
        trigrams[trigram] += 1

    popular_trigrams_freq = sum(trigrams[t] for t in popular_trigrams)
    popular_trigrams_freq /= sum(trigrams.values())
    if popular_trigrams_freq < 0.0038:
        return False
    return True


def decrypt_and_validate(ciphertext, common_bigrams):
    ciphertext_bigrams = get_bigrams(ciphertext)
    print("біграми мови: ", common_bigrams)
    print("біграми тексту: ", [k for k in ciphertext_bigrams.keys() ])
    candidates = generate_candidates(common_bigrams, ciphertext_bigrams)
    for candidate in candidates:
        decrypted_text = decrypt_text(ciphertext, candidate[1], candidate[2])
        if is_russian(decrypted_text):
            print(f"Ключі знайдено а:{candidate[0]} b:{candidate[2]}")
            print("Перші 100 букв тексту:")
            print(decrypted_text[:100])
            with open("results.txt", "w", encoding="utf8") as file:
                file.write(decrypted_text)
            break



common_bigrams = ["ст", "но", "то", "на", "ен"]


ciphertext = read_ciphertext("/home/liza/fti/3curs/kripto/kriptok/lab3k/07.txt")
ciphertext = re.sub(r'[^а-яА-Я ]', '', ciphertext.lower())  


decrypt_and_validate(ciphertext, common_bigrams)
