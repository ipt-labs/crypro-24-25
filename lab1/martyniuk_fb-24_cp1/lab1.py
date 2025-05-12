import re
from collections import Counter
import math
import csv
import pandas as pd

def format_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    text = re.sub(r'[^а-яё]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def remove_spaces(text):
    text = text.replace(' ', '')
    return text

def calculate_frequencies(text):
    # частоти букв
    letter_counts = Counter(text)
    total_letters = sum(letter_counts.values())
    letter_frequencies = {char: count / total_letters for char, count in letter_counts.items()}
    
    # частоти біграм з перетином 
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    bigram_counts = Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    bigram_frequencies = {bigram: count / total_bigrams for bigram, count in bigram_counts.items()}
    
    # частоти біграм без перетину 
    bigrams_non_overlapping = [text[i:i+2] for i in range(0, len(text) - 1, 2)]
    bigram_counts_no_overlap = Counter(bigrams_non_overlapping)
    total_bigrams_no_overlap = sum(bigram_counts_no_overlap.values())
    bigram_frequencies_no_overlap = {
        bigram: count / total_bigrams_no_overlap for bigram, count in bigram_counts_no_overlap.items()
    }
    
    return letter_frequencies, bigram_frequencies, bigram_frequencies_no_overlap

def calculate_entropy(frequencies):
    return -sum(p * math.log2(p) for p in frequencies.values() if p > 0)

def calculate_entropies(letter_freq, bigram_freq, bigram_freq_no_overlap):
    h1 = calculate_entropy(letter_freq)
    h2 = calculate_entropy(bigram_freq) / 2
    h2_no_overlap = calculate_entropy(bigram_freq_no_overlap) / 2
    return h1, h2, h2_no_overlap

def calculate_redundancy(entropy, alphabet_size):
    h_max = math.log2(alphabet_size)
    return 1 - entropy / h_max

def frequencies_to_csv(letter_freq, total_letters, output_file):
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(["Letter", "Count", "Frequency"])
        
        for letter, freq in sorted(letter_freq.items(), key=lambda x: -x[1]):
            count = round(freq * total_letters)
            frequency = f"{freq:.4f}"
            writer.writerow([letter, count, frequency])


def bigram_matrix(bigram_freq):
    # унікальні символи біграм
    symbols = sorted({bigram[0] for bigram in bigram_freq} | {bigram[1] for bigram in bigram_freq})
    matrix = pd.DataFrame(0.0, index=symbols, columns=symbols)
    
    for bigram, freq in bigram_freq.items():
        if len(bigram) == 2:
            matrix.loc[bigram[0], bigram[1]] = freq
    
    return matrix

def bigram_to_csv(matrix, filename="bigram_matrix.csv"):
    matrix.to_csv(filename, float_format="%.4f", encoding="utf-8")



file_path = "philos_aristo04.txt"

text_spaces = format_text(file_path)
letter_freq, bigram_freq, bigram_freq_no_overlap = calculate_frequencies(text_spaces)
h1_i, h2_i, h2_i_no_overlap = calculate_entropies(letter_freq, bigram_freq, bigram_freq_no_overlap)
total_letters = sum(Counter(text_spaces).values())  # загальна кількість букв
frequencies_to_csv(letter_freq, total_letters, 'monogram.csv')


text_no_spaces = remove_spaces(text_spaces)  
letter_freq_no_spaces, bigram_freq_no_spaces, bigram_freq_no_overlap_no_spaces = calculate_frequencies(text_no_spaces)
h1, h2, h2_no_overlap = calculate_entropies(letter_freq_no_spaces, bigram_freq_no_spaces, bigram_freq_no_overlap_no_spaces)
total_letters = sum(Counter(text_no_spaces).values())  
frequencies_to_csv(letter_freq_no_spaces, total_letters, 'monogram_no_spaces.csv')

alphabet_size = 34 # 33 літери + пробіл 
print("З пробілами:")
print(f"H1 (монограми): {h1_i:.4f}, R1: {calculate_redundancy(h1_i, alphabet_size):.4f}")
print(f"H2 (біграми, перекриття): {h2_i:.4f}, R2: {calculate_redundancy(h2_i, alphabet_size):.4f}")
print(f"H2 (біграми, без перекриття): {h2_i_no_overlap:.4f}, R2: {calculate_redundancy(h2_i_no_overlap, alphabet_size):.4f}")

alphabet_size = 33
print("\nБез пробілів:")
print(f"H1 (монограми): {h1:.4f}, R1: {calculate_redundancy(h1, alphabet_size):.4f}")
print(f"H2 (біграми, перекриття): {h2:.4f}, R2: {calculate_redundancy(h2, alphabet_size):.4f}")
print(f"H2 (біграми, без перекриття): {h2_no_overlap:.4f}, R2: {calculate_redundancy(h2_no_overlap, alphabet_size):.4f}")

matrix = bigram_matrix(bigram_freq)
bigram_to_csv(matrix, "bigram.csv")

matrix = bigram_matrix(bigram_freq_no_overlap)
bigram_to_csv(matrix, "bigram_no_overlap.csv")

matrix = bigram_matrix(bigram_freq_no_spaces)
bigram_to_csv(matrix, "bigram_no_spaces.csv")

matrix = bigram_matrix(bigram_freq_no_overlap_no_spaces)
bigram_to_csv(matrix, "bigram_no_spaces_no_overlap.csv")


#CoolPinkProgram
alphabet = 32
h10_low = 3.0625
h10_top = 3.3746

h20_low = 2.1685 
h20_top = 2.7445 

h30_low = 1.4038 
h30_top = 2.0713


print(f"\n{calculate_redundancy(h10_top,alphabet):.4f} < R10 < {calculate_redundancy(h10_low,alphabet):.4f}\n")
print(f"{calculate_redundancy(h20_top,alphabet):.4f} < R20 < {calculate_redundancy(h20_low,alphabet):.4f}\n")
print(f"{calculate_redundancy(h30_top,alphabet):.4f} < R30 < {calculate_redundancy(h30_low,alphabet):.4f}\n")
