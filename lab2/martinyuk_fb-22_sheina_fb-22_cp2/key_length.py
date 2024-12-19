import re
from collections import Counter

def calculate_ic(input_text):
    text_length = len(input_text)
    if text_length < 2:
        return 0
    
    char_counts = Counter(input_text)
    ic_value = sum(freq * (freq - 1) for freq in char_counts.values()) / (text_length * (text_length - 1))
    return ic_value

def divide_text_into_blocks(input_text, block_size):
    divided_blocks = [''] * block_size
    for index, character in enumerate(input_text):
        divided_blocks[index % block_size] += character
    return divided_blocks

def average_ic_for_block_size(input_text, block_size):
    blocks = divide_text_into_blocks(input_text, block_size)
    ic_values = [calculate_ic(block) for block in blocks]
    return sum(ic_values) / len(ic_values)

def identify_key_length(input_text, max_block_size=30):
    ic_results = {}
    for block_size in range(2, max_block_size + 1):
        ic_value = average_ic_for_block_size(input_text, block_size)
        ic_results[block_size] = ic_value
        print(f"Размер блока: {block_size}, IC: {ic_value}")
    
    return ic_results

def extract_text_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    filtered_content = re.sub(r'[^а-я]', '', content.lower())
    return filtered_content

file_name = "cryptext.txt"
encrypted_text = extract_text_from_file(file_name)

# Вычисляем индексы совпадений для различных длин ключа
ic_values = identify_key_length(encrypted_text, max_block_size=30)

# Определяем наиболее вероятные длины ключа
highest_ic = max(ic_values.values())
likely_key_lengths = [key_length for key_length, value in ic_values.items() if value == highest_ic]
print(f"\nНаиболее вероятная длинна ключа: {likely_key_lengths}")
