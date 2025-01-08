import pandas as pd
import math

# Символи з пробілом і без
chars_with_space = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
chars_without_space = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Читання та обробка тексту
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().replace('n', '').replace('\n', ' ').lower()

# Фільтрація тексту
def filter_text(input_text, charset, with_space=False):
    if with_space:
        return ''.join(symbol for symbol in input_text if symbol in charset and (symbol.isalpha() or symbol.isspace()))
    else:
        return ''.join(symbol for symbol in input_text if symbol in charset and symbol.isalpha())

# Підрахунок кількості та частоти символів
def calculate_char_count_and_freq(txt: str):
    count_dict = {}
    for char in txt:
        count_dict[char] = count_dict.get(char, 0) + 1
    
    total_length = len(txt)
    freq_dict = {char: round(count / total_length, 5) for char, count in count_dict.items()}
    
    return count_dict, freq_dict

# Функція для створення таблиці символів
def create_char_freq_df(count_dict, freq_dict):
    return pd.DataFrame({
        'Char': freq_dict.keys(),
        'Count': [count_dict[c] for c in freq_dict.keys()],
        'Freq': freq_dict.values()
    }).sort_values(by='Freq', ascending=False)

# Функція для підрахунку біграм
def calculate_bigram_count_and_freq(txt: str, overlap: bool):
    bigram_count = {}
    step = 1 if overlap else 2
    for i in range(0, len(txt) - 1, step):
        bigram = txt[i] + txt[i + 1]
        bigram_count[bigram] = bigram_count.get(bigram, 0) + 1

    total_bigrams = len(txt) - 1 if overlap else len(txt) // 2
    bigram_freq = {bg: round(count / total_bigrams, 5) for bg, count in bigram_count.items()}
    
    return bigram_count, bigram_freq

# Функція для створення таблиці біграм
def create_bigram_df(bigram_freq, charset):
    sorted_charset = sorted(charset)
    bigram_df = pd.DataFrame(index=sorted_charset, columns=sorted_charset)

    for bg in bigram_freq:
        x = sorted_charset.index(bg[0])
        y = sorted_charset.index(bg[1])
        bigram_df.iloc[x, y] = bigram_freq[bg]

    return bigram_df.rename(index={" ": "space"}, columns={" ": "space"}) if " " in bigram_df.index else bigram_df

# Функції для обчислення ентропії
def compute_entropy(freq_dict, n=2):
    entropy = -sum(freq * math.log2(freq) for freq in freq_dict.values() if freq > 0)
    return entropy / n

# Функція для обчислення надлишковості
def compute_redundancy(h, charset):
    h0 = math.log2(len(charset))
    return 1 - (h / h0)

# Основна логіка виконання
def main():
    file_path = 'lab1.txt'
    input_text = read_text(file_path)

    filtered_text = filter_text(input_text, chars_without_space)
    filtered_text_with_space = filter_text(input_text, chars_with_space, with_space=True)

    # Підрахунок частоти символів
    count_no_space, freq_no_space = calculate_char_count_and_freq(filtered_text)
    df_char_freq_no_space = create_char_freq_df(count_no_space, freq_no_space)
    print(df_char_freq_no_space)
    df_char_freq_no_space.to_excel("CharFreq_no_space.xlsx")

    count_with_space, freq_with_space = calculate_char_count_and_freq(filtered_text_with_space)
    df_char_freq_with_space = create_char_freq_df(count_with_space, freq_with_space)
    print(df_char_freq_with_space)
    df_char_freq_with_space.to_excel("CharFreq_with_space.xlsx")

    # Біграм
    bigram_count_overlap, bigram_freq_overlap = calculate_bigram_count_and_freq(filtered_text, True)
    bigram_df_overlap = create_bigram_df(bigram_freq_overlap, chars_without_space)
    print(bigram_df_overlap)
    bigram_df_overlap.to_excel("overlap_bigram.xlsx")

    bigram_count_overlap_space, bigram_freq_overlap_space = calculate_bigram_count_and_freq(filtered_text_with_space, True)
    bigram_df_overlap_space = create_bigram_df(bigram_freq_overlap_space, chars_with_space)
    print(bigram_df_overlap_space)
    bigram_df_overlap_space.to_excel("overlap_bigram_with_space.xlsx")

    bigram_count_nonoverlap, bigram_freq_nonoverlap = calculate_bigram_count_and_freq(filtered_text, False)
    bigram_df_nonoverlap = create_bigram_df(bigram_freq_nonoverlap, chars_without_space)
    print(bigram_df_nonoverlap)
    bigram_df_nonoverlap.to_excel("nonoverlap_bigram.xlsx")

    bigram_count_nonoverlap_space, bigram_freq_nonoverlap_space = calculate_bigram_count_and_freq(filtered_text_with_space, False)
    bigram_df_nonoverlap_space = create_bigram_df(bigram_freq_nonoverlap_space, chars_with_space)
    print(bigram_df_nonoverlap_space)
    bigram_df_nonoverlap_space.to_excel("nonoverlap_bigram_with_space.xlsx")

    # Ентропія
    h1_no_space = compute_entropy(freq_no_space, n=1)
    h1_with_space = compute_entropy(freq_with_space, n=1)
    print(f"Ентропія H1 для тексту без пробілів: {h1_no_space}")
    print(f"Ентропія H1 для тексту з пробілами: {h1_with_space}")

    h2_overlap = compute_entropy(bigram_freq_overlap, n=2)
    h2_overlap_space = compute_entropy(bigram_freq_overlap_space, n=2)
    h2_nonoverlap = compute_entropy(bigram_freq_nonoverlap, n=2)
    h2_nonoverlap_space = compute_entropy(bigram_freq_nonoverlap_space, n=2)

    print(f"Ентропія H2 для пересічних біграм (без пробілів): {h2_overlap}")
    print(f"Ентропія H2 для пересічних біграм (з пробілами): {h2_overlap_space}")
    print(f"Ентропія H2 для непересічних біграм (без пробілів): {h2_nonoverlap}")
    print(f"Ентропія H2 для непересічних біграм (з пробілами): {h2_nonoverlap_space}")

    # Надлишковість
    redundancy_h1 = compute_redundancy(h1_no_space, chars_without_space)
    redundancy_h1_space = compute_redundancy(h1_with_space, chars_with_space)
    redundancy_h2_overlap = compute_redundancy(h2_overlap, chars_without_space)
    redundancy_h2_overlap_space = compute_redundancy(h2_overlap_space, chars_with_space)
    redundancy_h2_nonoverlap = compute_redundancy(h2_nonoverlap, chars_without_space)
    redundancy_h2_nonoverlap_space = compute_redundancy(h2_nonoverlap_space, chars_with_space)

    print(f"Надлишковість H1 (без пробілів): {redundancy_h1}")
    print(f"Надлишковість H1 (з пробілами): {redundancy_h1_space}")
    print(f"Надлишковість H2 пересічні (без пробілів): {redundancy_h2_overlap}")
    print(f"Надлишковість H2 пересічні (з пробілами): {redundancy_h2_overlap_space}")
    print(f"Надлишковість H2 непересічні (без пробілів): {redundancy_h2_nonoverlap}")
    print(f"Надлишковість H2 непересічні (з пробілами): {redundancy_h2_nonoverlap_space}")

if __name__ == "__main__":
    main()
