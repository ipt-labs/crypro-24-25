import random
from collections import Counter

def generate_key(length):
    """Генерує випадковий ключ заданої довжини."""
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    return ''.join(random.choice(alphabet) for _ in range(length))

def vigenere_encrypt(text, key):
    """Шифрує текст за допомогою шифру Віженера."""
    encrypted_text = []
    key_length = len(key)
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    
    for i, char in enumerate(text):
        if char in alphabet:
            x_i = alphabet.index(char)
            k_i = alphabet.index(key[i % key_length])
            y_i = (x_i + k_i) % len(alphabet)
            encrypted_text.append(alphabet[y_i])
        else:
            encrypted_text.append(char) 
    
    return ''.join(encrypted_text)

def index_of_coincidence(text):
    """Обчислює індекс відповідності для заданого тексту."""
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    filtered_text = [char for char in text if char in alphabet]
    
    n = len(filtered_text)
    if n <= 1:
        return 0
    
    frequencies = Counter(filtered_text)
    numerator = sum(f * (f - 1) for f in frequencies.values())
    denominator = n * (n - 1)
    
    return numerator / denominator


keys = [generate_key(length) for length in [2, 3, 4, 5] + list(range(10, 21))]


with open("f.txt", "r", encoding="utf-8") as file:
    text = file.read()

open_text_ic = index_of_coincidence(text)
print(f"Індекс відповідності відкритого тексту: {open_text_ic:.16f}")


for key in keys:
    encrypted_text = vigenere_encrypt(text, key)
    encrypted_text_ic = index_of_coincidence(encrypted_text)
    print(f"Індекс відповідності шифртексту (ключ {len(key)} символів): {encrypted_text_ic:.16f}")
