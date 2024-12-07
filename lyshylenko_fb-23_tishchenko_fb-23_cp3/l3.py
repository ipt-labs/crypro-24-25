from collections import Counter
from itertools import permutations, combinations
from math import gcd

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
common_bigrams = ['ст', 'но', 'то', 'на', 'ен']
modulus = len(alphabet) ** 2

# Перетворення біграм у числа та навпаки
bigram_to_value = lambda bigram: (alphabet.index(bigram[0]) * len(alphabet) + alphabet.index(bigram[1])) % modulus
value_to_bigram = lambda num: alphabet[num // len(alphabet)] + alphabet[num % len(alphabet)]

# Генерація біграм
def generate_bigrams(input_text):
    return [input_text[i:i+2] for i in range(0, len(input_text) - 1, 2)]

# Розширений алгоритм Евкліда
def gcd_extended(a, b):
    while b:
        a, b = b, a % b
    return a

# Генерація всіх можливих співставлень
def permutations_with_mapping(src, target):
    return [{src[i]: perm[i] for i in range(len(src))} for perm in permutations(target)]

# Пошук найбільш частих біграм
def top_bigrams(bigram_counts, n):
    return bigram_counts.most_common(n)

# Обчислення коефіцієнта a
def compute_a(dy, dx, mod):
    return (dy * pow(dx, -1, mod)) % mod

# Розв’язання системи рівнянь для ключа
def solve_linear_congruence(pair):
    solutions = []
    y1, y2 = bigram_to_value(pair[0][0]), bigram_to_value(pair[1][0])
    x1, x2 = bigram_to_value(pair[0][1]), bigram_to_value(pair[1][1])
    dy, dx = (y1 - y2) % modulus, (x1 - x2) % modulus

    if dx == 0 or dy == 0:
        return []
    
    divisor = gcd_extended(dx, modulus)
    if divisor > 1:
        if dy % divisor != 0:
            return []
        dy //= divisor
        dx //= divisor
        modulus_reduced = modulus // divisor
    else:
        modulus_reduced = modulus

    base_a = compute_a(dy, dx, modulus_reduced)
    for k in range(divisor):
        a = (base_a + k * modulus_reduced) % modulus
        b = (y1 - x1 * a) % modulus
        solutions.append((a, b))
    
    return solutions

# Розшифрування біграми
def decrypt_bigram(bigram, key_a, key_b):
    num = bigram_to_value(bigram)
    decrypted = (num - key_b) * pow(key_a, -1, modulus) % modulus
    return value_to_bigram(decrypted)

# Чи є текст валідним
def is_valid_text(text_sample):
    consonants = 'бвгджзклмнпрстфхцчшщ'
    vowels = 'аеиоуыэюя'
    for i in range(len(text_sample) - 4):
        if (all(ch in consonants for ch in text_sample[i:i+5]) or 
            all(ch in vowels for ch in text_sample[i:i+5])):
            return False
    return True

# Читання шифртексту
raw_text = ""
with open("07.txt", 'r', encoding="utf8") as file:
    raw_text = "".join([char for line in file for char in line if char in alphabet])

# Обчислення біграм
bigrams_list = generate_bigrams(raw_text)
bigram_counts = Counter(bigrams_list)

# Пошук найчастіших біграм
popular_bigrams_with_counts = top_bigrams(bigram_counts, 5)
print("Найчастіші біграми шифртексту з кількістю появ:")
for bigram, count in popular_bigrams_with_counts:
    print(f"{bigram}: {count}")

# Отримання лише біграм без частоти
popular_bigrams = [bigram for bigram, _ in popular_bigrams_with_counts]

# Генерація можливих ключів
unique_pairs = set()
possible_permutations = permutations_with_mapping(popular_bigrams, common_bigrams)
for mapping in possible_permutations:
    unique_pairs.update(set(mapping.items()))

key_candidates = []
print("\nКандидати на ключі (a, b):")
for pair_combination in combinations(unique_pairs, 2):
    solutions = solve_linear_congruence(pair_combination)
    for solution in solutions:
        key_candidates.append(solution)
        print(f"Пари {pair_combination}: ключ {solution}")

# Валідація ключів та розшифрування
valid_keys = []
with open("decrypted_texts.txt", "w", encoding="utf8") as output_file:
    for key in set(key_candidates):
        test_decryption = ""
        full_decryption = ""
        for bigram in bigrams_list:  # Розшифровуємо весь текст
            try:
                decrypted_bigram = decrypt_bigram(bigram, key[0], key[1])
                test_decryption += decrypted_bigram
                full_decryption += decrypted_bigram
            except:
                break
        else:
            if is_valid_text(test_decryption[:200]):  # Перевірка тільки на першій частині тексту
                valid_keys.append(key)
                output_file.write(f"Ключ: {key}, Розшифрований текст: {full_decryption}\n\n")
                print(f"\nКлюч: {key}, Розшифрований текст записаний у файл.")