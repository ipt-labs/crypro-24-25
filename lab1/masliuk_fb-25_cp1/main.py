import math
import re
import pandas as pd
from collections import Counter

def preprocess_text(text, remove_spaces=False):
    text = text.lower()
    text = re.sub(r'[^а-яё ]', '', text)
    text = text.replace('ё', 'е')
    text = text.replace('ъ', 'ь')
    
    if remove_spaces:
        text = text.replace(' ', '')
    
    return text

def create_bigram_matrix(text, overlapping=True):
    unique_chars = sorted(set(text))
    n_chars = len(unique_chars)
    char_to_idx = {char: idx for idx, char in enumerate(unique_chars)}
    matrix = [[0] * n_chars for _ in range(n_chars)]
    
    if overlapping:
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
    else:
        bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    
    total_bigrams = len(bigrams)
    
    for bigram in bigrams:
        if len(bigram) == 2:
            i = char_to_idx[bigram[0]]
            j = char_to_idx[bigram[1]]
            matrix[i][j] += 1
    
    matrix = [[count/total_bigrams for count in row] for row in matrix]
    return matrix, unique_chars

def save_to_excel(text_with_spaces, text_without_spaces, filename='analysis_results.xlsx'):

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    workbook = writer.book
    number_format = workbook.add_format({'num_format': '0.0000'})
    
    #з пробілами
    letter_freq_spaces = calculate_letter_frequencies(text_with_spaces)
    letter_data_spaces = [{'літера': letter, 'частота': freq} 
                         for letter, freq in letter_freq_spaces.items()]
    df_letters_spaces = pd.DataFrame(letter_data_spaces)
    df_letters_spaces.to_excel(writer, sheet_name='Частоти літер (з пробілами)', index=False)
    
    # Без пробілів
    letter_freq_no_spaces = calculate_letter_frequencies(text_without_spaces)
    letter_data_no_spaces = [{'літера': letter, 'частота': freq} 
                            for letter, freq in letter_freq_no_spaces.items()]
    df_letters_no_spaces = pd.DataFrame(letter_data_no_spaces)
    df_letters_no_spaces.to_excel(writer, sheet_name='Частоти літер (без пробілів)', index=False)
    
    for sheet_name in ['Частоти літер (з пробілами)', 'Частоти літер (без пробілів)']:
        worksheet = writer.sheets[sheet_name]
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 12, number_format)
    
    bigram_variants = [
        ("Біграми (з пробілами, перекр.)", text_with_spaces, True),
        ("Біграми (без пробілів, перекр.)", text_without_spaces, True),
        ("Біграми (з пробілами, без перекр.)", text_with_spaces, False),
        ("Біграми (без пробілів, без перекр.)", text_without_spaces, False)
    ]
    
    for desc, text, overlapping in bigram_variants:
        bigram_freq = calculate_bigram_frequencies(text, overlapping)
        bigram_data = [{'біграма': bigram, 'частота': freq} 
                      for bigram, freq in bigram_freq.items()]
        df_bigrams = pd.DataFrame(bigram_data)
        
        sheet_name = desc[:31]
        df_bigrams.to_excel(writer, sheet_name=sheet_name, index=False)
        
        worksheet = writer.sheets[sheet_name]
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 12, number_format)
    
    writer.close()

def calculate_letter_frequencies(text):
    letter_counts = Counter(text)
    total_letters = len(text)
    
    frequencies = {letter: count/total_letters for letter, count in letter_counts.items()}
    frequencies = dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))

    return frequencies

def calculate_bigram_frequencies(text, overlapping=True):
    if overlapping:
        bigram_counts = Counter(text[i:i+2] for i in range(len(text)-1))
    else:
        bigram_counts = Counter(text[i:i+2] for i in range(0, len(text)-1, 2))
    
    total_bigrams = len(text) - 1 if overlapping else len(text) // 2
    
    frequencies = {bigram: count/total_bigrams for bigram, count in bigram_counts.items()}
    return frequencies

def calculate_entropy(frequencies):
    entropy = -sum(p * math.log2(p) for p in frequencies.values() if p > 0)
    return entropy

def calculate_redundancy(entropy, alphabet_size=32):
    max_entropy = math.log2(alphabet_size)
    redundancy = 1 - (entropy / max_entropy)
    return redundancy

def analyze_text(text):
    text_with_spaces = preprocess_text(text)
    
    text_without_spaces = preprocess_text(text, remove_spaces=True)
    
    print("Аналіз тексту з пробілами:")
    
    letter_freq_with_spaces = calculate_letter_frequencies(text_with_spaces)
    print("\nЧастоти літер (з пробілами):")
    for letter, freq in letter_freq_with_spaces.items():
        print(f"{letter}: {freq:.4f}")
    
    letter_entropy_with_spaces = calculate_entropy(letter_freq_with_spaces)
    letter_redundancy_with_spaces = calculate_redundancy(letter_entropy_with_spaces)
    
    print(f"\nЕнтропія літер у тексті з пробілами: {letter_entropy_with_spaces:.4f}")
    print(f"Надлишковість літер у тексті з пробілами: {letter_redundancy_with_spaces:.4f}")
    
    print("\nЧастоти літер (без пробілів):")
    letter_freq_without_spaces = calculate_letter_frequencies(text_without_spaces)
    for letter, freq in letter_freq_without_spaces.items():
        print(f"{letter}: {freq:.4f}")
    
    letter_entropy_without_spaces = calculate_entropy(letter_freq_without_spaces)
    letter_redundancy_without_spaces = calculate_redundancy(letter_entropy_without_spaces)
    
    print(f"\nЕнтропія літер у тексті без пробілів: {letter_entropy_without_spaces:.4f}")
    print(f"Надлишковість літер у тексті без пробілів: {letter_redundancy_without_spaces:.4f}")
    
    # Біграми
    bigram_types = [
        ("з пробілами, перекриваючі", text_with_spaces, True),
        ("без пробілів, перекриваючі", text_without_spaces, True),
        ("з пробілами, без перекриття", text_with_spaces, False),
        ("без пробілів, без перекриття", text_without_spaces, False)
    ]
    
    for description, text_variant, overlapping in bigram_types:
        print(f"\nБіграми ({description}):")
        bigram_freq = calculate_bigram_frequencies(text_variant, overlapping)

        print("Частоти біграм:")
        for bigram, freq in sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"{bigram}: {freq:.4f}")
        
        bigram_entropy = calculate_entropy(bigram_freq)
        bigram_redundancy = calculate_redundancy(bigram_entropy)
        
        print(f"Ентропія біграм: {bigram_entropy:.4f}")
        print(f"Надлишковість біграм: {bigram_redundancy:.4f}")

    with open("cleaned_text.txt", "w", encoding="utf-8") as file:
        file.write(text_without_spaces)
        print("\nОчищений текст збережено у файл 'cleaned_text.txt'.")
    
    save_to_excel(text_with_spaces, text_without_spaces)

if __name__ == "__main__":
    file_path = "TEXT"
    try:
        with open(file_path, "r", encoding="IBM866") as file:
            text_data = file.read()
        analyze_text(text_data)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено. Переконайтеся, що він існує.")
    except UnicodeDecodeError as e:
        print(f"Помилка декодування файлу: {e}")