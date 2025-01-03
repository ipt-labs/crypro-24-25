# Імпортуємо бібліотеки
import re

# Читаємо текстовий файл
file_path = 'text.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    original_text = file.read()

# Функція спрощення тексту
def simplify_text(text):
    # Видаляємо пунктуацію, пробіли та переводимо літери в нижній регістр
    text = re.sub(r'[^а-яё]', '', text.lower().replace('ё', 'е'))
    return text

# Функція шифрування шифром Віженера
def vigenere_encrypt(text, key):
    encrypted_text = []
    key_length = len(key)
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    m = len(alphabet)

    for i, char in enumerate(text):
        text_idx = alphabet.index(char)
        key_idx = alphabet.index(key[i % key_length])
        encrypted_char = alphabet[(text_idx + key_idx) % m]
        encrypted_text.append(encrypted_char)

    return ''.join(encrypted_text)

# Спрощуємо текст
simplified_text = simplify_text(original_text)

# Список ключів для шифрування
keys = {
    "key2": "да",
    "key3": "мир",
    "key4": "шифр",
    "key5": "роман",
    "key10": "саламандра",
    "key20": "благорасположенность"
}

# Створюємо словник для зашифрованих текстів
encrypted_texts = {k: vigenere_encrypt(simplified_text, v) for k, v in keys.items()}

# Збереження результатів у файли
output_files = {}
for key_name, encrypted_text in encrypted_texts.items():
    output_file = f"encrypted_{key_name}.txt"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
    output_files[key_name] = output_file

output_files