from collections import Counter
from itertools import permutations

# Константи та маппінги
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
CHAR_TO_NUM = {char: idx for idx, char in enumerate(ALPHABET)}
NUM_TO_CHAR = {idx: char for idx, char in enumerate(ALPHABET)}
RUSSIAN_CHAR_SET = set(CHAR_TO_NUM.keys())
FREQUENT_LETTERS = ['о', 'а', 'е']
RARE_LETTERS = ['ф', 'щ', 'ь']
COMMON_TRIGRAMS = {'про', 'сто', 'как', 'что', 'его'}
M = len(ALPHABET)

# Розширений алгоритм Евкліда
def extended_gcd(a, m):
    if a == 0:
        return m, 0, 1
    gcd, x1, y1 = extended_gcd(m % a, a)
    x = y1 - (m // a) * x1
    y = x1
    return gcd, x, y

# Обчислення оберненого елемента за модулем
def modular_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Немає оберненого елемента {a} за модулем {m}")
    return x % m

# Розв'язування лінійних порівнянь
def solve_linear_congruence(a, b, m):
    gcd, x, _ = extended_gcd(a, m)
    if b % gcd != 0:
        return []
    a1 = a // gcd
    b1 = b // gcd
    m1 = m // gcd
    x0 = (x * b1) % m1
    solutions = [(x0 + k * m1) % m for k in range(gcd)]
    return solutions

# Топ-5 біграм шифрованого тексту
def find_top_5_bigrams(cipher_text, step=2):
    bigram_counter = Counter()
    for i in range(0, len(cipher_text) - 1, step):
        bigram = cipher_text[i:i+2]
        bigram_counter[bigram] += 1
    return bigram_counter.most_common(5)

# Перетворення біграми на числове представлення
def bigram_to_number(bigram, char_to_num, m):
    x1 = char_to_num[bigram[0]]
    x2 = char_to_num[bigram[1]]
    number = x1 * m + x2
    return number

# Пошук можливих ключів
def solve_for_keys(language_bigrams, cipher_bigrams, char_to_num, m):
    m_squared = m * m
    candidates = []
    lang_nums = [bigram_to_number(bigram, char_to_num, m) for bigram in language_bigrams]
    cipher_nums = [bigram_to_number(bigram, char_to_num, m) for bigram in cipher_bigrams]
    for i in range(len(lang_nums)):
        for j in range(len(lang_nums)):
            if i == j:
                continue
            X1 = lang_nums[i]
            X2 = lang_nums[j]
            Y1 = cipher_nums[i]
            Y2 = cipher_nums[j]
            delta_X = (X1 - X2) % m_squared
            delta_Y = (Y1 - Y2) % m_squared
            solutions_a = solve_linear_congruence(delta_X, delta_Y, m_squared)
            for a in solutions_a:
                b = (Y1 - a * X1) % m_squared
                candidates.append((a, b))
    return candidates

# Дешифрування Афінного шифру
def decrypt_affine_bigram(cipher_text, a, b, char_to_num, num_to_char, m):
    m_squared = m * m
    decrypted_text = []
    a_inverse = modular_inverse(a, m_squared)
    for i in range(0, len(cipher_text) - 1, 2):
        bigram = cipher_text[i:i+2]
        if len(bigram) < 2:
            continue
        y = bigram_to_number(bigram, char_to_num, m)
        x = (a_inverse * (y - b)) % m_squared
        x1, x2 = divmod(x, m)
        decrypted_text.append(num_to_char[x1])
        decrypted_text.append(num_to_char[x2])
    return ''.join(decrypted_text)

# Розпізнавання змістовного тексту
def is_russian_text_advanced(text, char_set, frequent_letters, rare_letters, common_trigrams):
    valid_text = ''.join(char for char in text if char in char_set)
    total_chars = len(valid_text)
    if total_chars == 0:
        return False
    letter_freq = Counter(valid_text)
    total_trigrams = sum(valid_text.count(trigram) for trigram in common_trigrams)
    frequent_score = sum((letter_freq[char] / total_chars) for char in frequent_letters if char in letter_freq)
    rare_score = sum((letter_freq[char] / total_chars) for char in rare_letters if char in letter_freq)
    trigram_score = total_trigrams / (total_chars - 2) if total_chars > 2 else 0
    return frequent_score > 0.2 and rare_score < 0.05 and trigram_score > 0.01

# Головна функція
def main():
    with open('var_06_utf8.txt', 'r', encoding='utf-8') as file:
        cipher_text = ''.join(char for char in file.read() if char in CHAR_TO_NUM)

    print(f"\n => Шифрований текст (перші 200 символів):\n{cipher_text[:200]}\n")

    top_5_bigrams = find_top_5_bigrams(cipher_text)
    print(f"\n => Топ-5 біграм шифрованого тексту:\n => {top_5_bigrams}\n")

    language_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    cipher_bigrams = [bigram for bigram, _ in top_5_bigrams]

    # Генерація всіх комбінацій двох біграм з кожного списку
    lang_bigram_pairs = list(permutations(language_bigrams, 2))
    cipher_bigram_pairs = list(permutations(cipher_bigrams, 2))

    # counter = 0

    # Перебір всіх пар біграм і знаходження ключів
    for lang_pair in lang_bigram_pairs:
        for cipher_pair in cipher_bigram_pairs:
            try:
                keys = solve_for_keys(lang_pair, cipher_pair, CHAR_TO_NUM, M)
                counter += 1
                for a, b in keys:
                    decrypted_text = decrypt_affine_bigram(cipher_text, a, b, CHAR_TO_NUM, NUM_TO_CHAR, M)
                    if is_russian_text_advanced(decrypted_text, RUSSIAN_CHAR_SET, FREQUENT_LETTERS, RARE_LETTERS, COMMON_TRIGRAMS):
                        print(f"\n ==> Біграми ВТ: {lang_pair}\n ==> Біграми ШТ: {cipher_pair}\n")
                        print(f" ==> Ключ знайдений: (a={a}, b={b})")
                        print(" ==> Шифрований текст (перші 500 символів):\n")
                        print("*"*100)
                        print(decrypted_text[:500])
                        print("*"*100)
                        return
            except ValueError:
                continue

    # print(counter)

if __name__ == "__main__":
    main()