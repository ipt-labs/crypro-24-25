from collections import Counter
import re
from math_operations import *

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
invalid_bigrams = ['аь', 'оь', 'еы', 'иы', 'уь'] # Неіснуючі біграми

# Завантаження та очищення тексту
def load_and_clean_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text = text.lower()
            text = re.sub(r'[^' + re.escape(alphabet) + ' ]', '', text)
        return text
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено")
        return None

# Підрахунок біграм без перетинання
def count_bigrams_no_overlap(text):
    bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]  
    bigram_counts = Counter(bigrams)
    return bigram_counts

# Загальна кількість біграм
def count_total_bigrams(bigram_counts):
    return sum(bigram_counts.values())

# Частота біграм
def bigram_frequencies(bigram_counts, total_bigrams):
    frequencies = {bigram: count / total_bigrams for bigram, count in bigram_counts.items()}
    return frequencies

# Виведення топ-5 біграм
def print_top_5_bigrams(bigram_frequencies, i=False):
    top_5_bigrams = dict(sorted(bigram_frequencies.items(), key=lambda x: x[1], reverse=True)[:5])
    if i:
        print("Найчастіші біграми та їх частоти:")
        for bigram, frequency in top_5_bigrams.items():
            print(f"{bigram}: {frequency:.5f}")
    else:
        return top_5_bigrams

# Знаходження кандидатів для ключів
def keys_find(cipher_bigrams, plain_bigrams):
    m = 31
    keys = []
    for i in range(len(cipher_bigrams) - 1):
        for j in range(i + 1, len(cipher_bigrams)):
            for k in range(len(cipher_bigrams) - 1):
                for l in range(k + 1, len(cipher_bigrams)):
                    y1 = cipher_bigrams[i]
                    y2 = cipher_bigrams[j]
                    x1 = plain_bigrams[k]
                    x2 = plain_bigrams[l]
                    diff_y = (y1 - y2) % (m ** 2)
                    diff_x = (x1 - x2) % (m ** 2)
                    a_candidates = solve_linear_congruence(diff_x, diff_y, m ** 2)
                    print(a_candidates)
                    for a in a_candidates:
                        b = (y1 - a * x1) % (m ** 2)
                        keys.append((a, b))
    return keys


# Функція для дешифрування тексту
def decrypt_affine(ciphertext, a, b, m):

    a_inverse = extended_euclidean(a, m ** 2)
    if a_inverse is None:
        print(f"Обернений елемент для a={a} не існує, пропускаємо ключ (a, b) = ({a}, {b})")
        return None

    decrypted_text = []
    for i in range(0, len(ciphertext) - 2, 2):
        Y_i = alphabet.index(ciphertext[i]) * m + alphabet.index(ciphertext[i + 1])
        X_i = (a_inverse * (Y_i - b)) % (m ** 2)
        p2 = X_i % m
        p1 = (X_i - p2) // m
        decrypted_text.append(alphabet[p1])
        decrypted_text.append(alphabet[p2])

    return ''.join(decrypted_text)

#функція для перевірки змістовності тексту
def is_meaningful_text(text):
    for bigram in invalid_bigrams:
        if bigram in text:
            return False

    return True

def main(bigram_freq, ciphertext):
    candidates = []
    decrypted_texts = {}
    decrypted_var4 = []
    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Математичні операції")
        print("2. П'ять найчастіших біграм")
        print("3. Співставлення частот біграм") 
        print("4. Дешифрування тексту")
        print("5. Аналіз тексту на змістовність")
        print("6. Вийти")
        user_choice = input("Виберіть опцію: ").strip()
        if user_choice == '6':
            print(BLUE + " /}___/}❀\n( • . •)\n/ >    > Byeee" + RESET)
            break
        if user_choice == '1':
             while True:
                print(YELLOW + "\n-♥-Меню математичних операцій-♥-" + RESET)
                print("0. Повернутись")
                print("1. Обчислити обернений елемент(розш. алг. Евкліда)")
                print("2. Розв'язування лінійних порівнянь")

                text_choice = input("Виберіть опцію: ").strip()

                if text_choice == '1':
                    try:
                        print("\nВведіть натуральне значення для знаходження оберненого b ≡ a (mod n):")
                        a = int(input("Введіть число a: "))
                        n = int(input("Введіть модуль n: "))

                        if a <= 0 or n <= 0:
                            raise ValueError("Числа мають бути натуральними (додатними).")

                        b = extended_euclidean(a, n)
                        if b:
                            print(f"Обернений елемент числа {a} за модулем {n} дорівнює {b}")
                        else:
                            print(f"Оберненого елементу числа {a} за модулем {n} не існує.")

                    except ValueError as e:
                        print(e)

                elif text_choice == '2':
                    try:
                        print("\nВведіть значення для лінійного порівняння ax ≡ b (mod n):")
                        a = int(input("Введіть a: "))
                        b = int(input("Введіть b: "))
                        n = int(input("Введіть модуль n: "))

                        if a <= 0 or n <= 0 or b <= 0:
                            raise ValueError("Числа мають бути натуральними (додатними).")

                        solutions = solve_linear_congruence(a, b, n)
                        if solutions:
                            print("Розв'язки лінійного порівняння:", solutions)
                        else:
                            print("Порівняння не має розв'язків.")

                    except ValueError as e:
                        print(e)

                elif text_choice == '0':
                    break
                else:
                    print("Неправильний вибір. Спробуйте знову.")

        elif user_choice == '2':
            print_top_5_bigrams(bigram_freq, i=True)
        elif user_choice == '3':
            print("Можливі кандидати на ключі (a, b):")
            cipher_top_bigrams = list(print_top_5_bigrams(bigram_freq).keys())
            plain_top_bigrams = ['ст', 'но', 'то', 'на', 'ен']
            cipher_bigrams = [31 * alphabet.index(bigram[0]) + alphabet.index(bigram[1]) for bigram in cipher_top_bigrams]
            plain_bigrams = [31 * alphabet.index(bigram[0]) + alphabet.index(bigram[1]) for bigram in plain_top_bigrams]
            candidates = keys_find(cipher_bigrams, plain_bigrams)  # Зберігаємо кандидатів
            for candidate in candidates:
                print(candidate)

        elif user_choice == '4':
            if candidates:
                print("Дешифрування тексту для кожного кандидата ключа:")
                for a, b in candidates:
                    decrypted_text = decrypt_affine(ciphertext, a, b, len(alphabet))
                    decrypted_texts[(a, b)] = decrypted_text
                    print(f"Ключ (a={a}, b={b}): {decrypted_text[:100]}...")  # Виводимо перші 100 символів
            else:
                print("Кандидати для ключів не знайдені.")

        elif user_choice == '5':
            if decrypted_texts:
                for (a, b), text in decrypted_texts.items():
                    if is_meaningful_text(text):
                        decrypted_var4.append((a, b, text))
                        print(f"Змістовний текст (ключ: a={a}, b={b}): {text}")
                    else:
                        print(f"Знайдено не змістовний текст (ключ: a={a}, b={b}).")

                if decrypted_var4:
                    with open('decrypted_var4.txt', 'w', encoding='utf-8') as f:
                        for a, b, text in decrypted_var4:
                            f.write(f"Ключ: a={a}, b={b}\nТекст: {text}\n\n")
                    print("Змістовні тексти збережено у файл 'decrypted_var4.txt'.")
            else:
                print("Спочатку дешифруйте текст.")

        else:
            print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":

    ciphertext = load_and_clean_text('04.txt')
    bigram_counts = count_bigrams_no_overlap(ciphertext)
    total_bigrams = count_total_bigrams(bigram_counts)
    bigram_freq = bigram_frequencies(bigram_counts, total_bigrams)
    main(bigram_freq, ciphertext)
