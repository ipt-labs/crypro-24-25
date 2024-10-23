import math
from collections import Counter
import re
import chardet
import pandas as pd
from openpyxl.styles import Border, Side

# Визначення кодування файлу
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

# Читання тексту з файлу
def read_text(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read().lower()

# Очищення тексту (залишаємо тільки кириличні букви та пробіли)
def clean_text(text):
    text = re.sub(r'[^а-я ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

# Функція для підрахунку частот букв
def letter_frequency(text, alphabet):
    letter_counts = Counter(text)
    total_letters = sum(letter_counts.values())
    frequencies = {letter: letter_counts[letter] / total_letters if total_letters > 0 else 0 for letter in alphabet}
    return frequencies

# Функція для підрахунку частот біграм
def bigrams_frequency(text, alphabet, cross=True):
    frequencies = {}
    for first_letter in alphabet:
        for second_letter in alphabet:
            frequencies[first_letter + second_letter] = 0
    if cross:
        bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    else:
        bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]
    bigrams = [bigram for bigram in bigrams if len(bigram) == 2]
    bigram_counts = Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    for bigram, count in bigram_counts.items():
        frequencies[bigram] = count / total_bigrams if total_bigrams > 0 else 0
    return frequencies

# Функція для обчислення ентропії
def entropy(letter_frequencies, n):
    return -sum(p * math.log2(p) for p in letter_frequencies.values() if p > 0) / n

# Функція для обчислення надлишковості
def redundancy(H, alphabet):
    return 1 - (H / math.log2(len(alphabet)))

# Функція для запису частот в Excel файл
def save_frequencies_to_excel(letter_freqs, letter_freqs_no_spaces, bigram_freqs, bigram_freqs_no_spaces,
                              bigram_freqs_no_cross, bigram_freqs_no_spaces_no_cross,
                              H_values, R_values, alphabet, output_file_path):
    # Створення DataFrame для частот букв
    df_letters = pd.DataFrame(list(letter_freqs.items()))
    df_letters_no_spaces = pd.DataFrame(list(letter_freqs_no_spaces.items()))

    # Сортування DataFrame за алфавітом
    df_letters[0] = pd.Categorical(df_letters[0], categories=alphabet, ordered=True)
    df_letters_no_spaces[0] = pd.Categorical(df_letters_no_spaces[0], categories=alphabet, ordered=True)

    df_letters = df_letters.sort_values(0).reset_index(drop=True)
    df_letters_no_spaces = df_letters_no_spaces.sort_values(0).reset_index(drop=True)

    # Округлення частот до 6 знаків після коми
    df_letters[1] = df_letters[1].round(6)
    df_letters_no_spaces[1] = df_letters_no_spaces[1].round(6)

    # Створення матриць для біграм
    bigram_matrix = pd.DataFrame(0.0, index=alphabet, columns=alphabet)
    bigram_matrix_no_spaces = pd.DataFrame(0.0, index=alphabet, columns=alphabet)
    bigram_matrix_no_cross = pd.DataFrame(0.0, index=alphabet, columns=alphabet)
    bigram_matrix_no_spaces_no_cross = pd.DataFrame(0.0, index=alphabet, columns=alphabet)

    for bigram, freq in bigram_freqs.items():
        bigram_matrix.loc[bigram[0], bigram[1]] = freq

    for bigram, freq in bigram_freqs_no_spaces.items():
        bigram_matrix_no_spaces.loc[bigram[0], bigram[1]] = freq

    for bigram, freq in bigram_freqs_no_cross.items():
        bigram_matrix_no_cross.loc[bigram[0], bigram[1]] = freq

    for bigram, freq in bigram_freqs_no_spaces_no_cross.items():
        bigram_matrix_no_spaces_no_cross.loc[bigram[0], bigram[1]] = freq

    # Округлення матриць біграм до 6 знаків після коми
    bigram_matrix = bigram_matrix.round(6)
    bigram_matrix_no_spaces = bigram_matrix_no_spaces.round(6)
    bigram_matrix_no_cross = bigram_matrix_no_cross.round(6)
    bigram_matrix_no_spaces_no_cross = bigram_matrix_no_spaces_no_cross.round(6)

    # Створення матриці значень ентропії та надлишковості
    H_data = {
        'With spaces': [H_values['H1 (with spaces)'], H_values['H2 (with spaces, with cross)'],
                        H_values['H2 (with spaces, without cross)']],
        'Without spaces': [H_values['H1 (without spaces)'], H_values['H2 (without spaces, with cross)'],
                           H_values['H2 (without spaces, without cross)']],
    }
    R_data = {
        'With spaces': [R_values['R1 (with spaces)'], R_values['R2 (with spaces, with cross)'],
                        R_values['R2 (with spaces, without cross)']],
        'Without spaces': [R_values['R1 (without spaces)'], R_values['R2 (without spaces, with cross)'],
                           R_values['R2 (without spaces, without cross)']],
    }
    index_labels = ['H1', 'H2 (with cross)', 'H2 (without cross)']
    H_matrix = pd.DataFrame(H_data, index=index_labels)
    R_matrix = pd.DataFrame(R_data, index=index_labels)

    with pd.ExcelWriter(output_file_path) as writer:
        # Збереження частот букв
        df_letters.to_excel(writer, sheet_name='Letters (H1 spaces)', index=False, header=False)
        df_letters_no_spaces.to_excel(writer, sheet_name='Letters (H1)', index=False, header=False)

        # Збереження матриць частот біграм
        bigram_matrix.to_excel(writer, sheet_name='Bigrams (H2 spaces, cross)')
        bigram_matrix_no_spaces.to_excel(writer, sheet_name='Bigrams (H2 cross)')
        bigram_matrix_no_cross.to_excel(writer, sheet_name='Bigrams (H2 spaces)')
        bigram_matrix_no_spaces_no_cross.to_excel(writer, sheet_name='Bigrams (H2)')

        # Збереження ентропій
        df_H_matrix = H_matrix.reset_index()
        df_H_matrix.columns = [''] + df_H_matrix.columns[1:].tolist()
        df_H_matrix.to_excel(writer, sheet_name='H Values', index=False)

        # Збереження надлишковості
        df_R_matrix = R_matrix.reset_index()
        df_R_matrix.columns = [''] + df_R_matrix.columns[1:].tolist()
        df_R_matrix.to_excel(writer, sheet_name='R Values', index=False)

        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.freeze_panes = 'B2'  # Закріпити рядок 1 і стовпець 1

            # Автоматичне регулювання ширини стовпців
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = max(max_length, 10)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

                # Додаємо суцільну рамку
                thin = Side(border_style="thin", color="000000")
                for row in worksheet.iter_rows():
                    for cell in row:
                        cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)

if __name__ == "__main__":
    alphabet = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

    text = read_text("anna-karenina.txt")

    cleaned_text_spaces = clean_text(text)
    cleaned_text_no_spaces = cleaned_text_spaces.replace(" ", "")  # Вилучаємо пробіли

    letter_frequencies_spaces = letter_frequency(cleaned_text_spaces, alphabet + [' '])
    H1_spaces = entropy(letter_frequencies_spaces, 1)

    letter_frequencies_no_spaces = letter_frequency(cleaned_text_no_spaces, alphabet)
    H1_no_spaces = entropy(letter_frequencies_no_spaces, 1)

    bigram_frequencies_space_cross = bigrams_frequency(cleaned_text_spaces, alphabet + [' '])
    H2_spaces_cross = entropy(bigram_frequencies_space_cross, 2)

    bigram_frequencies_no_spaces_cross = bigrams_frequency(cleaned_text_no_spaces, alphabet)
    H2_no_spaces_cross = entropy(bigram_frequencies_no_spaces_cross, 2)

    bigram_frequencies_spaces_no_cross = bigrams_frequency(cleaned_text_spaces, alphabet + [' '], False)
    H2_spaces_no_cross = entropy(bigram_frequencies_spaces_no_cross, 2)

    bigram_frequencies_no_spaces_no_cross = bigrams_frequency(cleaned_text_no_spaces, alphabet, False)
    H2_no_spaces_no_cross = entropy(bigram_frequencies_no_spaces_no_cross, 2)

    H_values = {
        'H1 (with spaces)': H1_spaces,
        'H1 (without spaces)': H1_no_spaces,
        'H2 (with spaces, with cross)': H2_spaces_cross,
        'H2 (without spaces, with cross)': H2_no_spaces_cross,
        'H2 (with spaces, without cross)': H2_spaces_no_cross,
        'H2 (without spaces, without cross)': H2_no_spaces_no_cross,
    }

    R_values = {
        'R1 (with spaces)': redundancy(H1_spaces, alphabet + [' ']),
        'R1 (without spaces)': redundancy(H1_no_spaces, alphabet),
        'R2 (with spaces, with cross)': redundancy(H2_spaces_cross, alphabet + [' ']),
        'R2 (without spaces, with cross)': redundancy(H2_no_spaces_cross, alphabet),
        'R2 (with spaces, without cross)': redundancy(H2_spaces_no_cross, alphabet + [' ']),
        'R2 (without spaces, without cross)': redundancy(H2_no_spaces_no_cross, alphabet),
    }

    save_frequencies_to_excel(letter_frequencies_spaces, letter_frequencies_no_spaces,
                              bigram_frequencies_space_cross, bigram_frequencies_no_spaces_cross,
                              bigram_frequencies_spaces_no_cross, bigram_frequencies_no_spaces_no_cross,
                              H_values, R_values, alphabet, "frequencies.xlsx")
