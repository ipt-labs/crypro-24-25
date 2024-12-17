from collections import Counter

# Алфавіт і його розмір
ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя".replace("ё", "е").replace("ъ", "ь")
M = len(ALPHABET)


# Підрахунок частот біграм
def count_bigrams(text):
    return Counter([text[i:i + 2] for i in range(len(text) - 1)])


# Розширений алгоритм Евкліда для оберненого елемента
def mod_inverse(n):
    d, x, _ = extended_gcd(n, m := M ** 2)
    return x % m if d == 1 else None


def extended_gcd(n, x):
    if x == 0: return n, 1, 0
    d, x1, y1 = extended_gcd(x, n % x)
    return d, y1, x1 - (n // x) * y1


# Перетворення біграм у числа і навпаки
def bigram_to_number(bigram):
    return ALPHABET.index(bigram[0]) * M + ALPHABET.index(bigram[1])


def number_to_bigram(number):
    return ALPHABET[number // M] + ALPHABET[number % M]


# Дешифрування біграми
def affine_decrypt_bigram(bigram, a, b):
    a_inv = mod_inverse(a)
    if not a_inv: return None
    return number_to_bigram((a_inv * (bigram_to_number(bigram) - b)) % (M ** 2))


# Функція дешифрування тексту
def affine_decrypt(text, a, b):
    return ''.join(affine_decrypt_bigram(text[i:i + 2], a, b) or "" for i in range(0, len(text), 2))


# Автомат розпізнавання тексту
def is_meaningful_text(text):
    freq_letters = Counter(text)
    total = sum(freq_letters.values())
    common = sum(freq_letters[char] for char in {"о", "а", "е"})
    rare = sum(freq_letters[char] for char in {"ф", "щ", "ь"})
    return common / total >= 0.2 and rare / total <= 0.05


# Запис тексту у файл
def save_decrypted_text(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(text[i:i + 100] + "\n" for i in range(0, len(text), 100))


# Розв'язання лінійних порівнянь ax = b (mod m)
def solve_linear_congruence(a, b, m):
    d, x, _ = extended_gcd(a, m)
    if b % d != 0:
        return []  # Розв'язків немає
    x0 = (x * (b // d)) % m
    return [(x0 + i * (m // d)) % m for i in range(d)]


# Основна логіка
with open("07.txt", "r", encoding="utf-8") as file:
    ciphertext = ''.join(char for char in file.read().replace("\n", "") if char in ALPHABET)

cipher_bigrams = count_bigrams(ciphertext).most_common(5)

# Вивід 5 найчастіших біграм
print("5 найчастіших біграм у шифротексті:")
for bigram, count in cipher_bigrams:
    print(f"{bigram}: {count}")

language_bigrams = ["ст", "но", "то", "на", "ен"]

# Перебір ключів
for (cb1, _), (cb2, _) in [(x, y) for x in cipher_bigrams for y in cipher_bigrams if x != y]:
    for lb1, lb2 in [(x, y) for x in language_bigrams for y in language_bigrams if x != y]:
        X1, X2 = bigram_to_number(lb1), bigram_to_number(lb2)
        Y1, Y2 = bigram_to_number(cb1), bigram_to_number(cb2)
        for a in solve_linear_congruence(X1 - X2, Y1 - Y2, M ** 2):
            b = (Y1 - a * X1) % M ** 2
            plaintext = affine_decrypt(ciphertext, a, b)
            if plaintext and is_meaningful_text(plaintext):
                print(f"Знайдений ключ (a, b): {a}, {b}")
                save_decrypted_text("decrypted_text.txt", plaintext)
                exit()

print("Розшифрування не вдалося.")
