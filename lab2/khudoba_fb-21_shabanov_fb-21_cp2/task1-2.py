import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from tabulate import tabulate

rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def clean_text(text):
    text = re.sub(r'[^а-яё]', '', text.lower())
    text = text.replace('ё', 'е')
    return text

def vigenere_encrypt(plaintext, key):
    encrypted_text = []
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char in rus_alphabet:
            shift = rus_alphabet.index(key[i % key_length])
            idx = rus_alphabet.index(char)
            encrypted_char = rus_alphabet[(idx + shift) % len(rus_alphabet)]
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def generate_russian_key(length):
    sample_keys = {
        2: 'да',
        3: 'дом',
        4: 'свет',
        5: 'мирно',
        6: 'король',
        7: 'планета',
        8: 'переноси',
        9: 'сочинение',
        10: 'инновациян',
        11: 'партнёрство',
        12: 'природаведст',
        13: 'образованиеоб',
        14: 'технологиятехн',
        15: 'интеллектуалинт',
        16: 'взаимодействиевз',
        17: 'информационныйинф',
        18: 'профессиональныйко',
        19: 'взаимопониманиемоет',
        20: 'цекотдеревосаддерево'
    }
    return sample_keys[length]


with open('task1.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

cleaned_text = clean_text(raw_text)

output_folder = 'encrypt'
os.makedirs(output_folder, exist_ok=True)

keys = [generate_russian_key(length) for length in range(2, 21)]

for idx, key in enumerate(keys):
    print(f'Using key: {key}')  # Debug: Print the current key
    encrypted_text = vigenere_encrypt(cleaned_text, key)

    output_file = os.path.join(output_folder, f'encrypted_{idx + 2}.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted_text)

print("Шифрування завершено і знаходиться в папці: 'encrypt'.")
def index_of_coincidence(text):
    cleaned_text = clean_text(text)
    N = len(cleaned_text)

    if N == 0:  # Якщо текст порожній
        return 0

    freq = Counter(cleaned_text)
    IC = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return IC


# Зберігаємо індекси відповідності
ic_values = []

# Задаємо довжини ключів (r)
key_lengths = range(2, 21)

# Шлях до папки з шифртекстами
encrypt_folder = 'encrypt'

# Перебираємо всі шифртексти в папці encrypt
for key_length in key_lengths:
    filename = f'encrypted_{key_length}.txt'
    if filename in os.listdir(encrypt_folder):
        with open(os.path.join(encrypt_folder, filename), 'r', encoding='utf-8') as f:
            cipher_text = f.read()
            ic = index_of_coincidence(cipher_text)
            ic_values.append((key_length, ic))

# Формуємо таблицю
table = [["Довжина ключа (r)", "Індекс відповідності"]]
for key_length, ic in ic_values:
    table.append([key_length, f"{ic:.10f}"])

# Виводимо таблицю
print(tabulate(table, headers="firstrow", tablefmt="grid"))

# Діаграма
lengths = [row[0] for row in ic_values]
ics = [row[1] for row in ic_values]

plt.figure(figsize=(10, 6))
plt.plot(lengths, ics, marker='o')
plt.title('Індекс відповідності для різних довжин ключа (r)')
plt.xlabel('Довжина ключа (r)')
plt.ylabel('Індекс відповідності')
plt.xticks(lengths)
plt.grid()
plt.axhline(y=0.055, color='r', linestyle='--', label='IC відкритого тексту')
plt.legend()
plt.show()
