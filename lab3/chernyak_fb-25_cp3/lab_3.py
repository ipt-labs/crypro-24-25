import re
from itertools import product
from collections import Counter
from typing import List, Tuple

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alphabet)
m2 = m * m

alphabet_to_index = {ch: i for i, ch in enumerate(alphabet)}
index_to_alphabet = {i: ch for i, ch in enumerate(alphabet)}


def euclidean_algorithm(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    gcd, x, y = euclidean_algorithm(b % a, a)
    return gcd, y - (b // a) * x, x


def mod_inverse(a: int, m: int) -> int:
    gcd, x, _ = euclidean_algorithm(a, m)
    if gcd != 1:
        raise ValueError("Обернене за модулем не існує")
    return (x % m + m) % m


def congruence(a: int, b: int, m: int) -> List[int]:
    gcd, x0, _ = euclidean_algorithm(a, m)
    if b % gcd != 0:
        raise ValueError("Рівняння не має розв'язку")
    solutions = []
    x0 = (x0 * (b // gcd)) % m
    for i in range(gcd):
        solutions.append((x0 + i * (m // gcd)) % m)
    return solutions


def bigram_to_number(bigram: str) -> int:
    return alphabet_to_index[bigram[0]] * m + alphabet_to_index[bigram[1]]


def number_to_bigram(number: int) -> str:
    return index_to_alphabet[number // m] + index_to_alphabet[number % m]


def decrypt_text(ciphertext: str, key: Tuple[int, int]) -> str:
    a, b = key
    a_inv = mod_inverse(a, m2)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        bigram = ciphertext[i:i + 2]
        y = bigram_to_number(bigram)
        x = (a_inv * (y - b + m2)) % m2
        plaintext += number_to_bigram(x)
    return plaintext


def find_keys(ct: List[str], vt: List[str]) -> List[Tuple[int, int]]:
    keys = set()
    cipher_num = [bigram_to_number(bigram) for bigram in ct]
    plain_num = [bigram_to_number(bigram) for bigram in vt]
    for (y1, y2), (x1, x2) in product(product(cipher_num, repeat=2), product(plain_num, repeat=2)):
        if y1 == y2 or x1 == x2:
            continue
        delta_Y = (y1 - y2 + m2) % m2
        delta_X = (x1 - x2 + m2) % m2
        try:
            a_candidates = congruence(delta_X, delta_Y, m2)
            for a in a_candidates:
                b = (y1 - a * x1 + m2) % m2
                keys.add((a, b))
        except ValueError:
            continue
    return list(keys)


def read_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    text = re.sub(r"[^а-яА-Я]", "", text).lower()
    return text


def has_forbidden_bigrams(text: str, forbidden_bigrams: List[str]) -> bool:
    return any(bigram in text for bigram in forbidden_bigrams)


def top_bigrams(text: str, top_n: int = 5) -> List[Tuple[str, int]]:
    bigram_counts = Counter(text[i:i+2] for i in range(0, len(text) - 1, 2))
    return bigram_counts.most_common(top_n)


def main():
    ciphertext = read_text("./05_utf8.txt")
    print(f"Шифртекст: {ciphertext}")

    top5_bigrams = top_bigrams(ciphertext)
    print(f"Топ-5 біграм шифротексту: {top5_bigrams}")

    ct = [bigram for bigram, _ in top5_bigrams]
    vt = ["ст", "но", "то", "на", "ен"]
    keys = find_keys(ct, vt)

    forbidden_bigrams = ["аь", "юь", "еь", "оь"]
    for key in keys:
        try:
            decrypted_text = decrypt_text(ciphertext, key)
            if not has_forbidden_bigrams(decrypted_text, forbidden_bigrams):
                print(f"Ключ (a={key[0]}, b={key[1]}): {decrypted_text}")
                top_5 = top_bigrams(decrypted_text)
                print(f"Топ-5 біграм: {top_5}")
        except ValueError:
            continue
    print(f"Кількість знайдених ключів: {len(keys)}")
    print(list(keys))

if __name__ == "__main__":
    main()
