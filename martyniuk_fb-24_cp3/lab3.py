from itertools import permutations
import math

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
theoretical_bigrams = ('ст', 'но', 'то', 'на', 'ен')


def gcd_extended(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0


def modinv(a, m):
    gcd, x = gcd_extended(a, m)
    if gcd != 1:
        return None
    return x % m


def solve_linear_congruence(a, b, m):
    gcd, x0 = gcd_extended(a, m)
    if b % gcd != 0:
        return None

    a, b, m = a // gcd, b // gcd, m // gcd
    x0 = (x0 * b) % m

    return [(x0 + i * m) % (m * gcd) for i in range(gcd)]


def count_bigrams_from_text(text):
    bigram_counts = {}
    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        bigram_counts[bigram] = bigram_counts.get(bigram, 0) + 1

    return sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)[:5]


def count_a(x1, x2, y1, y2):
    x1 = alphabet.index(x1[0]) * len(alphabet) + alphabet.index(x1[1])
    x2 = alphabet.index(x2[0]) * len(alphabet) + alphabet.index(x2[1])

    y1 = alphabet.index(y1[0]) * len(alphabet) + alphabet.index(y1[1])
    y2 = alphabet.index(y2[0]) * len(alphabet) + alphabet.index(y2[1])

    results = solve_linear_congruence(y1 - y2, x1 - x2, len(alphabet) ** 2)
    if results:
        return [x for x in [modinv(i, len(alphabet) ** 2) for i in results] if x is not None]


def count_b(x1, y1, a):
    x1 = alphabet.index(x1[0]) * len(alphabet) + alphabet.index(x1[1])
    y1 = alphabet.index(y1[0]) * len(alphabet) + alphabet.index(y1[1])
    return (y1 - a * x1) % (len(alphabet) ** 2)


def all_possible_keys(cleaned_text, key_size=5):
    f_list = count_bigrams_from_text(cleaned_text)[:key_size]
    print(f"\n{f_list}\n")
    possible_keys = set()

    for i in permutations(theoretical_bigrams, 2):
        for j in range(len(f_list) - 1):
            key_1 = count_a(i[0], i[1], f_list[j][0], f_list[j + 1][0])
            if key_1 is None:
                continue

            for solution in key_1:
                key = (solution, count_b(i[0], f_list[j][0], solution))
                possible_keys.add(key)

    return list(possible_keys)


def decrypt(string, key):
    try:
        new_str = ''
        for i in range(0, len(string), 2):
            y = alphabet.index(string[i]) * len(alphabet) + alphabet.index(string[i + 1])
            x = (modinv(key[0], len(alphabet) ** 2) * (y - key[1])) % (len(alphabet) ** 2)
            new_str += alphabet[x // len(alphabet)] + alphabet[x % len(alphabet)]
        return new_str
    except (ValueError, TypeError):
        return None


def find_entropy(decrypted_text):
    entropy = 0.0
    total_letters = len(decrypted_text)
    letter_counts = {}

    for letter in decrypted_text:
        letter_counts[letter] = letter_counts.get(letter, 0) + 1

    for count in letter_counts.values():
        probability = count / total_letters
        entropy -= probability * math.log2(probability)

    return entropy


def check_the_text(decrypted_text):
    entropy = find_entropy(decrypted_text)
    return 4.2 < entropy < 4.5


def decrypt_and_check(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    cleaned_text = ''.join([char for char in text.lower() if char in alphabet])

    keys = all_possible_keys(cleaned_text)
    for key in keys:
        decrypted_text = decrypt(cleaned_text, key)
        if decrypted_text and check_the_text(decrypted_text):
            print(f"Decrypted text with key {key}:")
            print(decrypted_text)
            return

    print("No valid decryption found")


file_path = "11.txt"
decrypt_and_check(file_path)
