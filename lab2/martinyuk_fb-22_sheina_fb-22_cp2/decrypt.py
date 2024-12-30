import re
from collections import Counter

def calculate_ic(text):
    text_length = len(text)
    if text_length < 2:
        return 0
    
    char_frequencies = Counter(text)
    ic_value = sum(freq * (freq - 1) for freq in char_frequencies.values()) / (text_length * (text_length - 1))
    return ic_value


def divide_into_groups(text, group_size):
    groups = [''] * group_size
    for index, char in enumerate(text):
        groups[index % group_size] += char
    return groups


def average_ic_for_group_size(text, group_size):
    groups = divide_into_groups(text, group_size)
    ic_values = [calculate_ic(group) for group in groups]
    return sum(ic_values) / len(ic_values)


def determine_key_length(cipher_text, max_key_length=30):
    ic_results = {}
    for group_size in range(2, max_key_length + 1):
        ic_value = average_ic_for_group_size(cipher_text, group_size)
        ic_results[group_size] = ic_value
        print(f"Длина ключа: {group_size}, IC: {ic_value}")
    return ic_results


def decrypt_vigenere(cipher_text, decryption_key):
    plain_text = []
    decryption_key = decryption_key.lower()
    key_size = len(decryption_key)
    key_index = 0

    for symbol in cipher_text:
        if 'а' <= symbol <= 'я':
            shift = ord(decryption_key[key_index % key_size]) - ord('а')
            decrypted_symbol = chr((ord(symbol) - ord('а') - shift) % 32 + ord('а'))
            plain_text.append(decrypted_symbol)
            key_index += 1

    return ''.join(plain_text)


def derive_key(cipher_text, key_size):
    groups = divide_into_groups(cipher_text, key_size)
    derived_key = []

    for group in groups:
        char_freqs = Counter(group)
        most_frequent_char = char_freqs.most_common(1)[0][0]
        offset = (ord(most_frequent_char) - ord('о')) % 32
        derived_key.append(chr(ord('а') + offset))

    return ''.join(derived_key)


def load_ciphertext(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    only_letters = re.sub(r'[^а-я]', '', content.lower())
    return only_letters


file_name = "cryptext.txt" 
cipher_text = load_ciphertext(file_name)

# Найденный ключ для длины 12
key_for_length_12 = derive_key(cipher_text, 12)
print(f"\nНайденный ключ для длины 12: {key_for_length_12}")

# Расшифрованный текст с ключом длиной 12
decrypted_text_with_key_12 = decrypt_vigenere(cipher_text, "вшекспирбуря")
print(f"\nРасшифрованный текст с ключом длиной 12:\n{decrypted_text_with_key_12}")

# Найденный ключ для длины 24
key_for_length_24 = derive_key(cipher_text, 24)
print(f"\nНайденный ключ для длины 24: {key_for_length_24}")

# Расшифрованный текст с ключом длиной 24
decrypted_text_with_key_24 = decrypt_vigenere(cipher_text, key_for_length_24)
print(f"\nРасшифрованный текст с ключом длиной 24:\n{decrypted_text_with_key_24}")
