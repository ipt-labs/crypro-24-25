import re
import chardet
import os

def detect_file_encoding(file_path):
    """
    Визначає кодування файлу.
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def clean_text(file_path, output_path):
    """
    Очищує текст у файлі, залишаючи лише російські літери та перетворюючи їх у нижній регістр.
    """
    # Визначення кодування файлу
    file_encoding = detect_file_encoding(file_path)

    # Читання тексту
    with open(file_path, 'r', encoding=file_encoding) as file:
        text = file.read()

    # Очищення тексту
    cleaned_text = re.sub(r'[^а-я]', '', text.lower())

    # Збереження очищеного тексту
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"Очищений текст збережено у файл: {output_path}")
    return cleaned_text

def vigenere_encrypt(text, key):
    """
    Шифрує текст за допомогою шифру Віженера
    """
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alphabet_size = len(alphabet)
    encrypted_text = []
    
    key_indices = [alphabet.index(k) for k in key]
    key_length = len(key)

    for i, char in enumerate(text):
        if char in alphabet:
            text_index = alphabet.index(char)
            shift = key_indices[i % key_length]
            encrypted_char = alphabet[(text_index + shift) % alphabet_size]
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)  # Якщо символ не в алфавіті, залишаємо його без змін

    return ''.join(encrypted_text)

input_file_path = 'lab2.1.txt'
cleaned_file_path = 'cleaned_lab2.1.txt'
output_directory = 'encrypted'

# Очищуємо текст
cleaned_text = clean_text(input_file_path, cleaned_file_path)

# Ключі для шифрування
keys = {
    2: 'на',
    3: 'это',
    4: 'едва',
    5: 'сорок',
    10: 'содержание',
    11: 'переговоров',
    12: 'избалованных',
    13: 'присоединении',
    14: 'приехаввберлин',
    15: 'новосильцевузнал',
    16: 'завладениегенуей',
    17: 'милойэнтузиасткой',
    18: 'увлечениеидеальными',
    19: 'общественнымположением',
    20: 'необманутьожиданийлюдей'
}

# Шифруємо текст для кожного ключа
for length, key in keys.items():
    encrypted_text = vigenere_encrypt(cleaned_text, key)
    output_path = os.path.join(output_directory, f'encrypted_with_key_length_{length}.txt')
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)

    print(f"Текст зашифровано ключем довжиною {length}. Збережено у файл: {output_path}")
