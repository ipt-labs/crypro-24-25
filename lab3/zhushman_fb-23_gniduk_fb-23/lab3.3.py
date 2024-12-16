from collections import Counter

def extended_gcd(a, b):
    """Алгоритм Евкліда."""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1

def bigram_to_number(bigram, alphabet):
    return alphabet.index(bigram[0]) * len(alphabet) + alphabet.index(bigram[1])

def solve_modular_system(x1, y1, x2, y2, n):
    """Розв’язує систему рівнянь для знаходження (a, b)."""
    delta_x = (x1 - x2) % n
    delta_y = (y1 - y2) % n
    gcd, a_inv, _ = extended_gcd(delta_x, n)
    if gcd != 1:
        return []
    a = (delta_y * a_inv) % n
    b = (y1 - a * x1) % n
    return a, b

def find_candidates(language_bigrams, cipher_bigrams, alphabet):
    """Знаходить ключі (a, b) для пар біграм."""
    n = len(alphabet) ** 2
    candidates = []
    for lang_b1 in language_bigrams:
        for cipher_b1 in cipher_bigrams:
            x1, y1 = bigram_to_number(lang_b1, alphabet), bigram_to_number(cipher_b1, alphabet)
            for lang_b2 in language_bigrams:
                if lang_b2 == lang_b1:
                    continue
                for cipher_b2 in cipher_bigrams:
                    if cipher_b2 == cipher_b1:
                        continue
                    x2, y2 = bigram_to_number(lang_b2, alphabet), bigram_to_number(cipher_b2, alphabet)
                    try:
                        a, b = solve_modular_system(x1, y1, x2, y2, n)
                        candidates.append((a, b))
                    except ValueError:
                        continue
    return candidates

def modular_inverse(a, m):
    """Знаходить обернений елемент за модулем m."""
    gcd, x, _ = extended_gcd(a, m)
    return x % m if gcd == 1 else None

def decrypt(nums, a, b, m):
    """Дешифрує текст за допомогою ключа (a, b)."""
    decrypted_text = []
    a_inv = modular_inverse(a, m ** 2)
    if a_inv is None:
        return None
    for i in range(0, len(nums), 2):
        y = nums[i] * m + (nums[i + 1] if i + 1 < len(nums) else 0)
        x = (a_inv * (y - b)) % (m ** 2)
        decrypted_text.append(alphabet[x // m])
        decrypted_text.append(alphabet[x % m])
    return ''.join(decrypted_text)

def count_rare_bigrams(text, rare_bigrams):
    """Підрахунок кількості рідкісних біграм у тексті."""
    return sum(1 for i in range(0, len(text) - 1, 2) if text[i:i + 2] in rare_bigrams)

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
m = len(alphabet)
n = m ** 2
cipher_bigrams = ['вн', 'тн', 'дк', 'ун', 'хщ']
language_bigrams = ['ст', 'но', 'то', 'на', 'ен']
rare_bigrams = ['эм', 'эх', 'цб', 'эо', 'мф', 'щв', 'эи', 'бб', 'мэ', 'тб', 'кф', 'яы', 'цы', 'щд', 'жн', 'щл', 'гэ', 'уу', 'сф']

# Пошук кандидатів на ключ
candidates = find_candidates(language_bigrams, cipher_bigrams, alphabet)

with open('05.txt', 'r', encoding='utf-8') as f:
    ciphertext = f.read().replace('\n', '').strip()
nums = [alphabet.index(ch) for ch in ciphertext if ch in alphabet]

# Дешифрування тексту та підрахунок рідкісних біграм
results = {}
for a, b in candidates:
    decrypted_text = decrypt(nums, a, b, m)
    if decrypted_text:
        rare_count = count_rare_bigrams(decrypted_text, rare_bigrams)
        results[(a, b)] = (decrypted_text, rare_count)

# Сортування результатів за кількістю рідкісних біграм
sorted_results = sorted(results.items(), key=lambda x: x[1][1])

print("Можливі ключі (a, b):")
for key in candidates:
    print(key)

# Виведення ключів з найменшою кількістю рідкісних біграм
print("Ключі з найменшою кількістю рідкісних біграм:")
for i, ((a, b), (decrypted_text, rare_count)) in enumerate(sorted_results[:10], start=1):
    print(f"{i}. Ключ (a={a}, b={b}), Рідкісні біграми: {rare_count}")

# Виведення тексту для ключа з найменшою кількістю рідкісних біграм
best_key = sorted_results[0][0]
best_text = sorted_results[0][1][0]
print(f"\nТекст для ключа (a={best_key[0]}, b={best_key[1]}): {best_text}")

