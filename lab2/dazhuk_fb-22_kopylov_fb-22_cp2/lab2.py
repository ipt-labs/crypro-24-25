from collections import Counter
import re
import chardet
import pandas as pd
from openpyxl.styles import Alignment, Border, Side
import random
from itertools import product


# Визначення кодування файлу
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']


# Читання тексту з файлу
def read_text(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read().lower()


# Очищення тексту (залишаємо тільки кириличні букви та пробіли)
def clean_text(text):
    text = re.sub(r'[^а-я ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def vigenere(plaintext, key, alphabet, encrypt=True):
    encrypted_text = []
    alphabet_size = len(alphabet)
    key_length = len(key)

    if encrypt:
        # Шифрування
        operation = 1
    else:
        # Розшифрування
        operation = -1

    for i, char in enumerate(plaintext):
        char_index = alphabet.index(char)
        key_index = alphabet.index(key[i % key_length])
        encrypted_index = (char_index + key_index * operation) % alphabet_size
        encrypted_text.append(alphabet[encrypted_index])

    return ''.join(encrypted_text)


def index_of_coincidence(text):
    letter_counts = Counter(text)
    n = sum(letter_counts.values())
    total_sum = sum(Nt * (Nt - 1) for Nt in letter_counts.values())
    return total_sum / (n * (n - 1))


# Функція для знаходження оптимального значення r
def find_optimal_r(cipher_text, max_r=30):
    ioc_values = {}

    for r in range(1, max_r + 1):
        blocks = [''.join(cipher_text[i] for i in range(j, len(cipher_text), r)) for j in range(r)]
        ioc_per_block = [index_of_coincidence(block) for block in blocks]
        avg_ic = sum(ioc_per_block) / r
        ioc_values[r] = round(avg_ic, 4)

    return ioc_values


def find_letter_key(cipher_text, r, alphabet):
    blocks = [''.join(cipher_text[i] for i in range(j, len(cipher_text), r)) for j in range(r)]
    key = []

    # Індекс найімовірнішої літери мови (для російської це "о")
    x_index = alphabet.index('о')

    for block_num, block in enumerate(blocks, start=1):
        letter_counts = Counter(block)
        total_letters = sum(letter_counts.values())
        frequencies = {letter: letter_counts.get(letter, 0) / total_letters for letter in alphabet}

        # Сортуємо за частотою
        sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

        # Знаходимо букви, частоти яких близькі до максимальної частоти
        max_frequency = sorted_frequencies[0][1]
        close_frequencies = [letter for letter, freq in sorted_frequencies if abs(freq - max_frequency) <= 0.015]

        # Обчислюємо можливі значення ключа для кожного блоку
        block_keys = [(alphabet.index(letter) - x_index) % len(alphabet) for letter in close_frequencies]
        key.append(block_keys)

    keys = [''.join(alphabet[k] for k in key_comb) for key_comb in list(product(*key))]

    return keys


def save_to_excel(ioc_results, ioc_values, file_name="ioc_results.xlsx"):
    with pd.ExcelWriter(file_name, engine='openpyxl', mode='w') as writer:
        # Записуємо результати Індексу відповідності
        df_ioc = pd.DataFrame(list(ioc_results.items()), columns=['Довжина ключа', 'Індекс відповідності'])
        df_ioc.to_excel(writer, index=False, sheet_name="IOC Results")

        # Налаштовуємо вигляд стовпців у таблиці
        worksheet = writer.sheets["IOC Results"]
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                             top=Side(style='thin'), bottom=Side(style='thin'))
        for column in worksheet.columns:
            header_length = len(str(column[0].value))
            adjusted_width = header_length + 2
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            for cell in column:
                cell.alignment = Alignment(horizontal='center')
                cell.border = thin_border

        # Записуємо результати оптимального значення r
        df_ic = pd.DataFrame(list(ioc_values.items()), columns=['Довжина ключа', 'Індекс відповідності'])
        df_ic.to_excel(writer, index=False, sheet_name="Optimal r")

        # Налаштовуємо вигляд стовпців у таблиці
        worksheet = writer.sheets["Optimal r"]
        for column in worksheet.columns:
            header_length = len(str(column[0].value))
            adjusted_width = header_length + 2
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            for cell in column:
                cell.alignment = Alignment(horizontal='center')
                cell.border = thin_border



if __name__ == "__main__":
    alphabet = list('абвгдежзийклмнопрстуфхцчшщъыьэюя')
    text = read_text("anna-karenina.txt")[0:5000].replace(" ", "")
    cleaned_text = clean_text(text)

    with open("cleaned_text.txt", "w", encoding="utf-8") as file:
        file.write(cleaned_text)

    keys = [''.join(random.choice(alphabet) for _ in range(i)) for i in range(1, 21)]

    ioc_results = {}
    ioc_cleaned_text = index_of_coincidence(cleaned_text)
    ioc_results[0] = round(ioc_cleaned_text, 4)

    for key in keys:
        encrypted_text = vigenere(cleaned_text, key, alphabet, encrypt=True)
        ioc = index_of_coincidence(encrypted_text)
        ioc_results[len(key)] = round(ioc, 4)

    cipher_text = clean_text(read_text("cipher_text.txt"))

    # Знаходимо оптимальне значення r
    ioc_values = find_optimal_r(cipher_text)

    # Записуємо обидва результати в Excel
    save_to_excel(ioc_results, ioc_values)

    cipher_text = clean_text(read_text("cipher_text.txt"))
    optimal_r = 20

    # Знаходимо ключі
    keys = find_letter_key(cipher_text, optimal_r, alphabet)
    with open("keys.txt", "w", encoding="utf-8") as file:
        for key in keys:
            file.write(f"{key}\n")
    key = "улановсеребряныепули"

    plaintext = vigenere(cipher_text, key, alphabet, encrypt=False)

    print(cipher_text[0:40])
    print(key*2)
    print(plaintext[0:40])