import re
from collections import Counter
import math
import pandas as pd

def calculate_frequencies(text, n=1):
    text = re.sub(r'[^а-яА-Я]', '', text).lower()
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    frequencies = Counter(ngrams)
    total = sum(frequencies.values())
    return {k: v / total for k, v in frequencies.items()}

def calculate_entropy(frequencies):
    return -sum(p * math.log2(p) for p in frequencies.values())

def save_frequencies_to_file(frequencies, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for item, freq in sorted(frequencies.items()):
            file.write(f"{item}: {freq:.6f}\n")

def save_bigram_table_to_excel(frequencies, file_name):
    bigram_matrix = {}

    for bigram, freq in frequencies.items():
        row, col = bigram[0], bigram[1]
        if row not in bigram_matrix:
            bigram_matrix[row] = {}
        bigram_matrix[row][col] = freq

    rows = sorted(bigram_matrix.keys())
    cols = sorted(set(col for row in bigram_matrix.values() for col in row))

    data = []
    for row in rows:
        data.append([bigram_matrix[row].get(col, 0) for col in cols])
    df = pd.DataFrame(data, index=rows, columns=cols)
    df.to_excel(file_name)

def analyze_text_with_spaces(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    letter_frequencies = calculate_frequencies(text, n=1)
    H1 = calculate_entropy(letter_frequencies)

    bigram_frequencies = calculate_frequencies(text, n=2)
    H2 = calculate_entropy(bigram_frequencies) / 2

    save_frequencies_to_file(letter_frequencies, 'letter_with_gaps.txt')
    save_bigram_table_to_excel(bigram_frequencies, 'bigram_with_gap.xlsx')

    return H1, H2, letter_frequencies, bigram_frequencies

def analyze_text_without_spaces(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_no_spaces = file.read()

    letter_frequencies_no_spaces = calculate_frequencies(text_no_spaces, n=1)
    H1_no_spaces = calculate_entropy(letter_frequencies_no_spaces)

    bigram_frequencies_no_spaces = calculate_frequencies(text_no_spaces, n=2)
    H2_no_spaces = calculate_entropy(bigram_frequencies_no_spaces) / 2

    save_frequencies_to_file(letter_frequencies_no_spaces, 'letter_without_gaps.txt')
    save_bigram_table_to_excel(bigram_frequencies_no_spaces, 'bigram_without_gap.xlsx')

    return H1_no_spaces, H2_no_spaces, letter_frequencies_no_spaces, bigram_frequencies_no_spaces

file_path_with_spaces = 'text.txt'  
file_path_without_spaces = 'text_without_gaps.txt'  

H1, H2, letter_frequencies, bigram_frequencies = analyze_text_with_spaces(file_path_with_spaces)
H1_no_spaces, H2_no_spaces, letter_frequencies_no_spaces, bigram_frequencies_no_spaces = analyze_text_without_spaces(file_path_without_spaces)

print("H1:", H1)
print("H2:", H2)
print("H1 (no gap):", H1_no_spaces)
print("H2 (no gap):", H2_no_spaces)
