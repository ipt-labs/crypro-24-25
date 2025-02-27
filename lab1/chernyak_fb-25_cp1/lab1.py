import re
import pandas as pd
import numpy as np
from collections import Counter
from math import log2


def preprocess_text(text, remove_spaces=False):
    text = text.lower()
    text = re.sub(r'[^а-яё ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    if remove_spaces:
        text = text.replace(" ", "")
    return text


def calculate_frequencies(text):
    letter_counts = Counter(text)
    total_letters = sum(letter_counts.values())
    letter_freq = {char: count / total_letters for char, count in letter_counts.items()}

    # Створюємо алфавіт
    alphabet = sorted(set(text) - {" "})

    # Матриця частот біграм
    bigram_matrix = pd.DataFrame(0, index=alphabet, columns=alphabet)
    for i in range(len(text) - 1):
        if text[i] in alphabet and text[i + 1] in alphabet:
            bigram_matrix.at[text[i], text[i + 1]] += 1

    # Нормалізація матриці
    total_bigrams = bigram_matrix.values.sum()
    bigram_matrix = bigram_matrix / total_bigrams

    return letter_freq, bigram_matrix


def entropy(frequencies):
    if isinstance(frequencies, dict):
        return -sum(freq * log2(freq) for freq in frequencies.values() if freq > 0)
    elif isinstance(frequencies, pd.DataFrame):
        return -np.sum(frequencies.values * np.log2(frequencies.values + 1e-10))


def save_to_csv(data, filename, index_label=None, columns_label=None):
    if isinstance(data, pd.DataFrame):
        data.to_csv(filename, index_label=index_label)
    else:
        df = pd.DataFrame.from_dict(data, orient='index', columns=[columns_label])
        df = df.sort_values(by=columns_label, ascending=False)
        df.to_csv(filename, index_label=index_label)


def main():
    with open("input_text.txt", "r", encoding="utf-8") as file:
        text = file.read()

    cleaned_text_with_spaces = preprocess_text(text, remove_spaces=False)
    cleaned_text_without_spaces = preprocess_text(text, remove_spaces=True)

    letter_freq_with_spaces, bigram_matrix_with_spaces = calculate_frequencies(cleaned_text_with_spaces)
    letter_freq_without_spaces, bigram_matrix_without_spaces = calculate_frequencies(cleaned_text_without_spaces)

    H1_with_spaces = entropy(letter_freq_with_spaces)
    H2_with_spaces = entropy(bigram_matrix_with_spaces) / 2

    H1_without_spaces = entropy(letter_freq_without_spaces)
    H2_without_spaces = entropy(bigram_matrix_without_spaces) / 2

    print("Ентропія для тексту з пробілами (включно з пробілами в H1):")
    print(f"H1 (ентропія букв): {H1_with_spaces}")
    print(f"H2 (ентропія біграм): {H2_with_spaces}")

    print("\nЕнтропія для тексту без пробілів:")
    print(f"H1 (ентропія букв): {H1_without_spaces}")
    print(f"H2 (ентропія біграм): {H2_without_spaces}")

    save_to_csv(letter_freq_with_spaces, "letter_frequencies_with_spaces.csv", index_label="Літера",
                columns_label="Частота")
    save_to_csv(bigram_matrix_with_spaces, "bigram_matrix_with_spaces.csv", index_label="Перша літера")
    save_to_csv(letter_freq_without_spaces, "letter_frequencies_without_spaces.csv", index_label="Літера",
                columns_label="Частота")
    save_to_csv(bigram_matrix_without_spaces, "bigram_matrix_without_spaces.csv", index_label="Перша літера")


if __name__ == "__main__":
    main()
