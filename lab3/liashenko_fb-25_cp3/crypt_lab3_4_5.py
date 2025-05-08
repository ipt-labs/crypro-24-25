import re
from collections import Counter
import itertools

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alphabet)

def extended_euclidean(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_euclidean(b, a % b)
    return g, y1, x1 - (a // b) * y1

def mod_inverse(a, m):
    g, x, _ = extended_euclidean(a, m)
    return x % m if g == 1 else -1

def solve_linear_congruence(a, b, m):
    g, _, _ = extended_euclidean(a, m)
    if b % g != 0:
        return []
    a, b, m = a // g, b // g, m // g
    inv = mod_inverse(a, m)
    return [(inv * b + i * m) % (m * g) for i in range(g)] if inv != -1 else []

def get_bigrams(text):
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 2)]
    return Counter(bigrams)

def generate_candidates(common_bigrams, ciphertext_bigrams):
    top_ciphertext_bigrams = sorted(ciphertext_bigrams, key=ciphertext_bigrams.get, reverse=True)[:5]
    pairs = {((alphabet.index(c[0]) * m + alphabet.index(c[1])) % m**2,
              (alphabet.index(t[0]) * m + alphabet.index(t[1])) % m**2)
             for c in common_bigrams for t in top_ciphertext_bigrams}
    
    return {(a, mod_inverse(a, m**2), (y1 - a * x1) % m**2)
            for (x1, y1), (x2, y2) in itertools.combinations(pairs, 2)
            for a in solve_linear_congruence((x1 - x2) % m**2, (y1 - y2) % m**2, m**2)
            if mod_inverse(a, m**2) != -1}

def decrypt_text(ciphertext, a, b):
    decrypted = ""
    for i in range(0, len(ciphertext) - 1, 2):
        y = alphabet.index(ciphertext[i]) * m + alphabet.index(ciphertext[i+1])
        x = (a * (y - b)) % m**2
        decrypted += alphabet[x // m] + alphabet[x % m]
    return decrypted

def index_of_coincidence(text):
    n = len(text)
    return sum(v * (v - 1) for v in Counter(text).values()) / (n * (n - 1)) if n > 1 else 0

def have_sense(text):    
    freqs = Counter(text)
    common_letters = ["о", "а", "е"]
    uncommon_letters = ["ф", "щ", "ь"]
    
    freq_of_common_letters = sum(freqs[letter] for letter in common_letters if letter in freqs) / len(text)
    freq_of_uncommon_letters = sum(freqs[letter] for letter in uncommon_letters if letter in freqs) / len(text)
    ic = index_of_coincidence(text)
    
    if ic < 0.04:
        return False
    if freq_of_uncommon_letters > 0.07:
        return False
    if freq_of_common_letters < 0.15:
        return False

    return True

def decrypt_and_validate(ciphertext, common_bigrams):
    ciphertext_bigrams = get_bigrams(ciphertext)
    print("10 найчастіших біграм у шифротексті:")
    print(ciphertext_bigrams.most_common(10))
    
    candidates = generate_candidates(common_bigrams, ciphertext_bigrams)
    print(f"Знайдено кандидатів для ключів: {len(candidates)}")

    for candidate in candidates:
        a, a_inv, b = candidate
        decrypted = decrypt_text(ciphertext, a_inv, b)
        ic = index_of_coincidence(decrypted)
        print(f"Ключ: a={a}, b={b}, IC={ic:.4f}")
        
        if have_sense(decrypted):
            print(f"\nЗнайдено підходящий ключ: a={a}, b={b}")
            print("Перші 150 символів дешифрування:")
            print(decrypted[:150])
            
            with open("results.txt", "w", encoding="utf8") as file:
                file.write(decrypted)
            break
    else:
        print("Підходящого варіанту не знайдено.")

# Основна частина
common_bigrams = ["ст", "но", "ен", "то", "на"]

with open('08.txt', "r", encoding="utf-8") as file:
    ciphertext = re.sub(r'[^а-яА-Я]', '', file.read().lower())

decrypt_and_validate(ciphertext, common_bigrams)

