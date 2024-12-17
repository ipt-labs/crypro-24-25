from collections import Counter
import matplotlib.pyplot as plt
import re

def index_of_coincidence(text):
    """
    Обчислює індекс відповідності тексту.
    """
    n = len(text)
    if n <= 1:
        return 0
    frequencies = Counter(text)
    numerator = sum(f * (f - 1) for f in frequencies.values())
    denominator = n * (n - 1)
    return numerator / denominator

def determine_key_length(text, max_key_length=30):
    """
    Знаходить оптимальну довжину ключа шляхом аналізу індексів відповідності.
    """
    optimal_length = 0
    minimal_difference = float('inf')
    ic_values = {}
    theoretical_ic = 0.0557  # Теоретичний IC для російського тексту

    for length in range(2, max_key_length + 1):
        average_ic = sum(index_of_coincidence(text[i::length]) for i in range(length)) / length
        ic_values[length] = average_ic
        difference = abs(average_ic - theoretical_ic)

        if difference < minimal_difference:
            minimal_difference = difference
            optimal_length = length

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.bar(ic_values.keys(), ic_values.values(), color='blue', alpha=0.7)
    plt.axhline(theoretical_ic, color='red', linestyle='--', label='Теоретичний IC')
    plt.title("Індекси відповідності для різних довжин ключа")
    plt.xlabel("Довжина ключа")
    plt.ylabel("IC")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    return optimal_length, ic_values

def recover_key(text, key_length):
    """
    Знаходить ключ за допомогою частотного аналізу.
    """
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    most_common_letter = "о"
    key = []

    for i in range(key_length):
        block = text[i::key_length]
        most_common_char = Counter(block).most_common(1)[0][0]
        key_char = (alphabet.index(most_common_char) - alphabet.index(most_common_letter)) % len(alphabet)
        key.append(alphabet[key_char])

    return ''.join(key)

def vigenere_decrypt(cipher_text, key):
    """
    Розшифровує текст за допомогою шифру Віженера.
    """
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    decrypted_text = []
    key_length = len(key)

    for i, char in enumerate(cipher_text):
        if char in alphabet:
            shift = alphabet.index(key[i % key_length])
            decrypted_char = alphabet[(alphabet.index(char) - shift) % len(alphabet)]
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)

# Зчитуємо зашифрований текст
input_file = 'lab2.3.txt'
output_file = 'decrypted_lab2.3.txt'

with open(input_file, 'r', encoding='utf-8') as file:
    cipher_text = file.read().replace('ё', 'е')

# Визначаємо довжину ключа
key_length, ic_values = determine_key_length(cipher_text)
print(f"Оптимальна довжина ключа: {key_length}")

# Знаходимо ключ
key = recover_key(cipher_text, key_length)
print(f"Знайдений ключ: {key}")

# Розшифровуємо текст
decrypted_text = vigenere_decrypt(cipher_text, key)

# Зберігаємо результат у файл
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(decrypted_text)

print(f"Розшифрування завершено. Текст збережено у файл: {output_file}")
