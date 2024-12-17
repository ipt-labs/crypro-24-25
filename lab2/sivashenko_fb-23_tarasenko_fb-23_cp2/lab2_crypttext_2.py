import re
from collections import Counter


def index_of_coincidence(text):
    n = len(text)
    if n < 2:
        return 0
    
    freqs = Counter(text)
    ic = sum(count * (count - 1) for count in freqs.values()) / (n * (n - 1))
    return ic


def split_into_blocks(ciphertext, period):
    blocks = [''] * period
    for i, char in enumerate(ciphertext):
        blocks[i % period] += char
    return blocks


def average_ic_for_period(ciphertext, period):
    blocks = split_into_blocks(ciphertext, period)
    ic_values = [index_of_coincidence(block) for block in blocks]
    return sum(ic_values) / len(ic_values)


def find_key_length(ciphertext, max_period=30):
    ics = {}
    for period in range(2, max_period + 1):
        ic = average_ic_for_period(ciphertext, period)
        ics[period] = ic
        print(f"Період: {period}, IC: {ic}")
    return ics


def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key = key.lower()  
    key_length = len(key)
    key_index = 0

    for char in ciphertext:
        if 'а' <= char <= 'я':  
            shift = ord(key[key_index % key_length]) - ord('а') 
            decrypted_char = chr((ord(char) - ord('а') - shift) % 32 + ord('а'))
            decrypted_text.append(decrypted_char)
            key_index += 1

    return ''.join(decrypted_text)

def find_key(ciphertext, key_length):
    blocks = split_into_blocks(ciphertext, key_length)
    key = []

    for block in blocks:
        freqs = Counter(block)
        most_common_letter = freqs.most_common(1)[0][0]  
        shift = (ord(most_common_letter) - ord('о')) % 32  
        key.append(chr(ord('а') + shift))

    return ''.join(key)

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    letters = re.sub(r'[^а-я]', '', text.lower())
    return letters

file_path = "cryptext.txt" 
ciphertext = read_text(file_path)

key_length_14 = find_key(ciphertext, 14)
print(f"\nЗнайдений ключ для довжини 14: {key_length_14}")


decrypted_text_14 = vigenere_decrypt(ciphertext, "последнийдозор")
print(f"\nРозшифрований текст з ключем довжиною 14:\n{decrypted_text_14}")






