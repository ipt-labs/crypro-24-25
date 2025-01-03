import collections
import math
import csv
import re

# Функція для підрахунку частоти літер
def let_freq(text):
    letter_counts = collections.Counter(text)
    total_letters = sum(letter_counts.values())
    letter_frequencies = {char: count / total_letters for char, count in letter_counts.items()}
    return letter_counts, letter_frequencies

# Функція для підрахунку біграм з або без перетину
def bi_freq(text, overlap=False):
    if overlap:
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
    else:
        bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    bigram_counts = collections.Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    bigram_frequencies = {bigram: count / total_bigrams for bigram, count in bigram_counts.items()}
    return bigram_counts, bigram_frequencies

# Функція для обчислення ентропії H1
def calculate_H1(letter_frequencies):
    return -sum(frequency * math.log2(frequency) for frequency in letter_frequencies.values())

# Функція для обчислення ентропії H2
def calculate_H2(bigram_frequencies):
    return -sum(frequency * math.log2(frequency) for frequency in bigram_frequencies.values()) / 2

# Функція для запису результатів
def to_csv(filename, counts, frequencies):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Symbol', 'Count', 'Frequency'])
        for symbol, count in counts.items():
            writer.writerow([symbol, count, frequencies[symbol]])

# Функція для підготовки тексту, видаляємо непотрібні символи 
def pre_for_text(text, with_spaces=True):
    text = text.lower()  
    if with_spaces:
        # Залишаємо тільки малі букви російського алфавіту та пробіли
        text = re.sub(r'[^а-яё ]', '', text)
    else:
        # Залишаємо тільки малі букви російського алфавіту, без пробілів
        text = re.sub(r'[^а-яё]', '', text)
    return text

# Основна функція для обчислення частот і ентропії
def proc_for_text(text, with_spaces=True):
    # Підготовка тексту
    processed_text = pre_for_text(text, with_spaces=with_spaces)

    # Частоти літер
    letter_counts, letter_frequencies = let_freq(processed_text)
    to_csv(f'letter_frequencies_{"with" if with_spaces else "without"}_spaces.csv', letter_counts, letter_frequencies)

    # Біграми без перетину
    bigram_counts_bez_peretuny, bigram_bez_peretuny = bi_freq(processed_text, overlap=False)
    to_csv(f'bigram_bez_peretuny_{"with" if with_spaces else "without"}_spaces.csv', bigram_counts_bez_peretuny, bigram_bez_peretuny)

    # Біграми з перетином
    bigram_counts_z_peretunom, bigram_freqz_peretunom = bi_freq(processed_text, overlap=True)
    to_csv(f'bigram_z_peretunom_{"with" if with_spaces else "without"}_spaces.csv', bigram_counts_z_peretunom, bigram_freqz_peretunom)

    H1 = calculate_H1(letter_frequencies)
    H2_bez_peretuny = calculate_H2(bigram_bez_peretuny)
    H2_z_peretunom = calculate_H2(bigram_freqz_peretunom)

    return H1, H2_bez_peretuny, H2_z_peretunom

# Завантаження тексту з файлу
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def main():
    file_path = 'text_russian.txt'  
    text = load_text(file_path)

    # Обробка тексту з пробілами
    print("Обробка тексту з пробілами...")
    H1_with_spaces, H2_bez_peretuny_with_spaces, H2_z_peretunom_with_spaces = proc_for_text(text, with_spaces=True)

    # Обробка тексту без пробілів
    print("Обробка тексту без пробілів...")
    H1_without_spaces, H2_bez_peretuny_without_spaces, H2_z_peretunom_without_spaces = proc_for_text(text, with_spaces=False)

    # Виведення результатів
    print("Результат записано у CSV файли")
    print(f"Ентропія H1 з пробілами: {H1_with_spaces}")
    print(f"Ентропія H2 без перетину з пробілами: {H2_bez_peretuny_with_spaces}")
    print(f"Ентропія H2 з перетином з пробілами: {H2_z_peretunom_with_spaces}")

    print(f"Ентропія H1 без пробілів: {H1_without_spaces}")
    print(f"Ентропія H2 без перетину без пробілів: {H2_bez_peretuny_without_spaces}")
    print(f"Ентропія H2 з перетином без пробілів: {H2_z_peretunom_without_spaces}")

main()
