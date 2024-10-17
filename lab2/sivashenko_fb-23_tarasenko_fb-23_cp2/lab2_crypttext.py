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

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    letters = re.sub(r'[^а-я]', '', text.lower())
    return letters

file_path = "cryptext.txt"
ciphertext = read_text(file_path)

# Знаходимо індекси відповідності для різних довжин ключа
ics = find_key_length(ciphertext, max_period=30)

# Шукаємо найбільш ймовірну довжину ключа
max_ic = max(ics.values())
probable_periods = [k for k, v in ics.items() if v == max_ic]
print(f"\nЙмовірні довжини ключа: {probable_periods}")
