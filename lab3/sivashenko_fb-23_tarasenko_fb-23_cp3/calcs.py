import re
from collections import defaultdict, Counter
import math

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Обернений елемент не існує, оскільки НСД({a}, {m}) ≠ 1")
    else:
        return x % m

def solve_linear_congruence(a, b, m):
    g, x, _ = extended_gcd(a, m)
    if g == 1:
        x0 = (mod_inverse(a, m) * b) % m
        return [x0]
    elif b % g == 0:
        x0 = (x * (b // g)) % m
        solutions = [(x0 + i * (m // g)) % m for i in range(g)]
        return solutions
    else:
        return False

def bigram_to_number(bigram, m):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    if len(bigram) != 2:  
        raise ValueError("Біграм має містити два символи.")
    return alphabet.index(bigram[0]) * m + alphabet.index(bigram[1])

def find_potential_keys(freq_bigrams_russian, freq_bigrams_cipher, m):
    m_squared = m**2
    possible_keys = []
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

    for bigram_rus1 in freq_bigrams_russian:
        for bigram_rus2 in freq_bigrams_russian:
            if bigram_rus1 == bigram_rus2:
                continue

            for bigram_cipher1 in freq_bigrams_cipher:
                for bigram_cipher2 in freq_bigrams_cipher:
                    if bigram_cipher1 == bigram_cipher2:
                        continue 

                    # Перетворюємо біграми в числове представлення
                    X1 = bigram_to_number(bigram_rus1, m)
                    X2 = bigram_to_number(bigram_rus2, m)
                    Y1 = bigram_to_number(bigram_cipher1, m)
                    Y2 = bigram_to_number(bigram_cipher2, m)

                    # Виконуємо розрахунок ключів
                    key_first_part = solve_linear_congruence(X1 - X2, Y1 - Y2, m_squared)
                    if key_first_part != False:
                        for elem in key_first_part:
                            if math.gcd(elem, len(alphabet)) == 1:
                                key_second_part = (Y1 - elem * X1) % m_squared
                                if [elem, key_second_part] not in possible_keys:
                                    possible_keys.append([elem, key_second_part])
                                    print(f"Знайдені ключі: a={elem}, b={key_second_part}")

    return possible_keys


def decrypt_text(ciphertext, a, b, m):
    alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
    m_squared = m ** 2
    decrypted_text = ""
    for i in range(0, len(ciphertext) - 2, 2):
        Y = alphabet.index(ciphertext[i]) * m + alphabet.index(ciphertext[i + 1])
        a1 = mod_inverse(a, m ** 2)
        X = (a1 * (Y - b)) % (m ** 2)
        x2 = X % m
        x1 = (X - x2) // m
        decrypted_text = decrypted_text + alphabet[x1] + alphabet[x2]
    return decrypted_text

def calculate_entropy(text):
    freq = Counter(text)
    text_len = len(text)
    entropy = 0.0
    
    for count in freq.values():
        p = count / text_len
        entropy -= p * math.log2(p)
    
    return entropy

def decrypt_and_filter_by_entropy(ciphertext, possible_keys, m):
    valid_keys_with_entropy = {}

    for a, b in possible_keys:
        try:
            decrypted_text = decrypt_text(ciphertext, a, b, m)
            entropy = calculate_entropy(decrypted_text)
            if entropy >= 4.40 and entropy <= 4.50:
                key_str = f"a={a}, b={b}"
                valid_keys_with_entropy[key_str] = entropy
                print(f"Ключ: {key_str}, Ентропія: {entropy}")
                return decrypt_text(ciphertext, a, b, 31)
        except ValueError as e:
            continue    
    return valid_keys_with_entropy

with open("text.txt", 'r', encoding='utf-8') as file:
    ciphertext = file.read().strip()
    ciphertext = re.sub(r'[^а-яА-ЯёЁ]', '', ciphertext)

freq_bigrams_cipher = list(Counter([ciphertext[i:i + 2] for i in range(0, len(ciphertext) - 1, 2)]).most_common(5))
print(f"Часті біграми у шифротексті: {[bigram[0] for bigram in freq_bigrams_cipher]}")

freq_bigrams_russian = ['ст', 'но', 'то', 'на', 'ен']

m = 31

possible_keys = find_potential_keys(freq_bigrams_russian, [bigram[0] for bigram in freq_bigrams_cipher], m)
print(f"Кількість можливих пар ключів: {len(possible_keys)}")
decrypted = decrypt_and_filter_by_entropy(ciphertext, possible_keys, m)
print('[!] ДО: ')
print(ciphertext)
print('[!] ПІСЛЯ: ')
print(decrypted)
