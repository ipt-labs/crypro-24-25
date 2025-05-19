import re
from collections import Counter

ciphered_file = '11.txt'
decrypted_file = 'res_v-11.txt'

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
alphabet_length = len(alphabet)
bigram_modulus = alphabet_length**2

common_bigrams = ['ст', 'но', 'то', 'на', 'ен']
frequent_letters = ['о', 'е', 'а']
rare_letters = ['ф', 'щ', 'ь']

def clean_text(text, remove_spaces=False):
    text = text.lower()
    text = re.sub(r'[^а-яё ]', '', text)
    text = text.replace('ё', 'е').replace('ъ', 'ь')
    return text.replace(' ', '') if remove_spaces else text

def calculate_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modular_inverse(a, mod, values=None):
    if values is None:
        values = [0, 1]
    if a == 0 or calculate_gcd(a, mod) != 1:
        return None
    else:
        remainder = mod % a
        quotient = mod // a
        values.append((values[-2] - quotient * values[-1]))
        if remainder != 0:
            mod, a = a, remainder
            return modular_inverse(a, mod, values)
        else:
            return values[-2]

def solve_linear_congruence(a, b, n, solutions=None):
    if solutions is None:
        solutions = []
    a, b = a % n, b % n
    divisor = calculate_gcd(a, n)
    if divisor == 1:
        inverse = modular_inverse(a, n)
        if inverse is not None:
            solutions.append((inverse * b) % n)
        return solutions
    elif divisor > 1 and b % divisor == 0:
        a1, b1, n1 = a // divisor, b // divisor, n // divisor
        solve_linear_congruence(a1, b1, n1, solutions)
        for i in range(1, divisor):
            first_solution = solutions[0]
            next_solution = (first_solution + n1 * i) % n
            solutions.append(next_solution)
        return solutions
    else:
        return None

print("18^(-1) mod 35: ", modular_inverse(18, 35, None))
print("3^(-1) mod 11: ", modular_inverse(3, 11, None), '\n')

print("3x = 9 mod 12: ", *solve_linear_congruence(3, 9, 12, None))
print("4x = 6 mod 10: ", *solve_linear_congruence(4, 6, 10, None), '\n')

def get_frequent_bigrams(text, option):
    bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]
    bigram_counts = {bigram: bigrams.count(bigram) / len(bigrams) for bigram in set(bigrams)}
    if option == 1:
        sorted_bigrams = sorted(bigram_counts.items(), key=lambda item: item[1], reverse=True)
        return [bigram for bigram, freq in sorted_bigrams[:5]]
    else:
        return dict(sorted(bigram_counts.items(), key=lambda item: item[1], reverse=True))

def bigram_to_number(bigram):
    try:
        return alphabet.index(bigram[0]) * alphabet_length + alphabet.index(bigram[1])
    except ValueError:
        return None

def validate_decrypted_text(text):
    score = 0
    char_counts = Counter(text)
    sorted_chars = dict(sorted(char_counts.items(), key=lambda item: item[1], reverse=True))
    
    frequent_in_text = list(sorted_chars.keys())[:3]
    rare_in_text = list(sorted_chars.keys())[-3:]
    score += sum(1 for char in frequent_in_text if char in frequent_letters)
    score += sum(1 for char in rare_in_text if char in rare_letters)
    
    bigrams_in_text = get_frequent_bigrams(text, 1)
    score += sum(1 for bigram in bigrams_in_text if bigram in common_bigrams)
    
    return score

def decrypt_text(data, a, b):
    decrypted = ""
    for i in range(0, len(data) - 1, 2):
        bigram = data[i:i + 2]
        Y = bigram_to_number(bigram)
        if Y is None:
            continue
        X = solve_linear_congruence(a, Y - b, bigram_modulus, None)[0]
        first_letter = X // alphabet_length
        second_letter = X % alphabet_length
        decrypted += alphabet[first_letter] + alphabet[second_letter]
    return decrypted

def find_keys(ciphered_text, common_bigrams, output_file):
    ciphered_bigrams = get_frequent_bigrams(ciphered_text, 1)
    print("Найчастіші біграми: ", ciphered_bigrams)
    possible_keys = []
    found_decrypted_texts = set()
    
    for i in range(len(common_bigrams)):
        for j in range(len(common_bigrams)):
            for q in range(len(ciphered_bigrams)):
                for w in range(len(ciphered_bigrams)):
                    if i != j and q != w:
                        X1, X2 = bigram_to_number(common_bigrams[i]), bigram_to_number(common_bigrams[j])
                        Y1, Y2 = bigram_to_number(ciphered_bigrams[q]), bigram_to_number(ciphered_bigrams[w])
                        if None in (X1, X2, Y1, Y2):
                            continue
                        X_diff, Y_diff = X1 - X2, Y1 - Y2
                        inverse = modular_inverse(X_diff, bigram_modulus, None)
                        if inverse is not None:
                            a_values = solve_linear_congruence(X_diff, Y_diff, bigram_modulus, None)
                            if a_values is not None:
                                for a in a_values:
                                    if a > 0 and modular_inverse(a, bigram_modulus, None) is not None:
                                        b = (Y1 - a * X1) % bigram_modulus
                                        if b > 0:
                                            decrypted_text = decrypt_text(ciphered_text, a, b)
                                            if decrypted_text not in found_decrypted_texts:
                                                possible_keys.append((a, b))
                                                found_decrypted_texts.add(decrypted_text)
                                                if validate_decrypted_text(decrypted_text) > 7:
                                                    print(f'Ключ a = {a}, b = {b}')
                                                    print("Розшифрований текст: ", decrypted_text)
                                                    output_file.write(decrypted_text)
    return possible_keys

with open(ciphered_file, 'r', encoding='utf-8') as file:
    ciphered_text = clean_text(file.read(), remove_spaces=True)

with open(decrypted_file, 'w', encoding='utf-8') as output:
    find_keys(ciphered_text, common_bigrams, output)
