import sys

sys.path.insert(1, 'lab1/prysievok_fb_23_kushnaryov_fb_23_cp1/')

import lab1
import math
from collections import Counter

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

def letter_to_number(letter):
    return alphabet.index(letter.lower())

def number_to_letter(number):
    return alphabet[number]

def bigram_to_number(bigram, m=len(alphabet)):
    return letter_to_number(bigram[0]) * m + letter_to_number(bigram[1])

def number_to_bigram(number):
    return alphabet[number // len(alphabet)] + alphabet[number % len(alphabet)]

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None  # Обернений елемент не існує
    return x % m

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def solve_linear_congruence(a, b, m):
    gcd, x, _ = extended_gcd(a, m)
    if b % gcd != 0:
        return None  # Немає рішень
    
    x0 = (x * (b // gcd)) % m
    solutions = []
    for i in range(gcd):
        solutions.append((x0 + i * (m // gcd)) % m)
    return solutions

def solve_affine_key(bigrams_cipher, bigrams_language, m=len(alphabet)):
    keys = []
    n = len(bigrams_cipher)
    list_c = []
    list_l = []
    for i in range(n):
        for j in range(i+1, n):
            list_c.append((bigrams_cipher[i], bigrams_cipher[j]))
    for k in range(n):
        for l in range(k+1, n):
            list_l.append((bigrams_language[k], bigrams_language[l]))

    for i in range(len(list_c)):
        for j in range(len(list_l)):
            x1 = bigram_to_number(list_l[j][0])
            x2 = bigram_to_number(list_l[j][1])
            y1 = bigram_to_number(list_c[i][0])
            y2 = bigram_to_number(list_c[i][1])

            list_a = solve_linear_congruence(x1-x2, y1-y2, m**2)
            if list_a:
                for a in list_a:
                    keys.append((a, (y1 - x1*a)%m**2))
    return keys

def decrypt_affine(text, a, b, m=len(alphabet)):
    a_inv = mod_inverse(a, m**2)
    if a_inv is None:
        return None  # If a_inv doesn't exist, skip this key
    decrypted = ""
    for i in range(0, len(text), 2):
        bigram = text[i:i+2]
        y = bigram_to_number(bigram)
        x = (a_inv * (y - b)) % m**2
        decrypted += number_to_bigram(x)
    return decrypted
    



def is_meaningful(text, forbidden_grams, frequent_grams, entropy_threshold):

    def text_entropy(text):
        counts = Counter(text)
        total = sum(counts.values())
        return -sum((count / total) * math.log2(count / total) for count in counts.values())

    result = True
    # Check impossible bigrams
    for gram in forbidden_grams:
        if gram in text:
             result = False
    
    # Check frequent l-grams
    frequent_count = sum(text.count(gram) for gram in frequent_grams)
    if frequent_count < len(frequent_grams) / 2:  # Example threshold
         result = False
    
    # Check entropy
    entropy = text_entropy(text)
    if entropy < entropy_threshold:
         result = False

    return result

def guess_affine_key_and_decrypt(keys, ciphertext, forbidden_grams, frequent_grams, entropy_threshold=3.5):
    candidates = []
    # Attempt to decrypt and filter meaningful texts
    for a, b in keys:
        decrypted_text = decrypt_affine(ciphertext, a, b, len(alphabet))
        if decrypted_text and is_meaningful(decrypted_text, forbidden_grams, frequent_grams, entropy_threshold):
            candidates.append((a, b, decrypted_text))
    
    return candidates



if __name__ == "__main__":
    text_cipher_path = 'tasks/cp3/variants.utf8/06.txt'
    text_lang_path = 'lab1/prysievok_fb_23_kushnaryov_fb_23_cp1/alice.txt'
    raw_text = lab1.read_txt_file(text_lang_path)
    raw_text_cipher = lab1.read_txt_file(text_cipher_path)
    text_alice = lab1.clean_text_no_spaces(raw_text)
    text_cipher = lab1.clean_text_no_spaces(raw_text_cipher)

    # Приклад використання
    n = 6
    print(f"\n Top {6} bigrams")
    language_bigrams = lab1.get_top_n_bigrams(lab1.get_bigrams_no_overlap(text_alice), n)
    cipher_bigrams = lab1.get_top_n_bigrams(lab1.get_bigrams_no_overlap(text_cipher), n)

    print(f"In language:    {language_bigrams}")
    print(f"In cipher text: {cipher_bigrams}")

    # Знаходимо ключі
    keys = solve_affine_key(list(cipher_bigrams.keys()), list(language_bigrams.keys()))

    # Example usage
    forbidden_grams = ["аь", "оь", 'аы', "эи", "жы", "чы"]   # Example forbidden bigrams
    frequent_grams = ["ст", "но", "ен"]  # Example frequent bigrams

    candidates = guess_affine_key_and_decrypt(keys, text_cipher, forbidden_grams, language_bigrams)
    if len(candidates) == 0:
        print(f"no candidates for {len(keys)} keys")
    else:
        print('\nDecrypted candidates:')
        for i in range(len(candidates)):
            a, b, text = candidates[i]
            print(f"{i}. a: {a}, b: {b}, Decrypted text: {text[:50]}")
        
        id_to_write = int(input('Type candidate`s id to save it to file: '))
        if id_to_write in range(len(candidates)):
            with open('lab3/prysievok_fb_23_kushnaryov_fb_23_cp3/decrypted.txt', 'w') as file: 
                _, _, text = candidates[id_to_write]
                file.write(text) 
                print('File saved')

    # plaintext = decrypt_affine(text_cipher, 441, 310)
    # print("Decrypted text:", plaintext[:30])
