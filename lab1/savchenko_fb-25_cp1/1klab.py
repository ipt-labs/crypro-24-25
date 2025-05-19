import re
from collections import Counter, defaultdict
import math
import pandas as pd

# Функція для обчислення ентропії
def calculate_entropy(values):
    total_count = sum(values)
    return -sum((count / total_count) * math.log2(count / total_count) for count in values)

# Читання тексту
with open('/home/liza/fti/3curs/kripto/kriptok/lab3k/07.txt', "r", encoding="utf-8") as file:
    my_text = file.read()

my_text = re.sub(r'\s+', ' ', my_text)

# Обробка тексту з пробілами
with_space = re.sub(r'[^а-яА-Я ]', '', my_text).lower()
text_len = len(with_space)

# Частоти букв з пробілами
frequencies_with_spaces = Counter(with_space)

# Підрахунок біграм без перекриття
bigram_counts_with_spaces = defaultdict(int)
for i in range(0, text_len - 1, 2):
    bigram_counts_with_spaces[with_space[i:i+2]] += 1

# Підрахунок біграм з перекриттям
bigram_counts_overlap_with_spaces = defaultdict(int)
for i in range(text_len - 1):
    bigram_counts_overlap_with_spaces[with_space[i:i+2]] += 1

# 5 найчастіших біграм з пробілами
top_5_bigrams_with_spaces = Counter(bigram_counts_overlap_with_spaces).most_common(5)

# Ентропія H1 та H2 для тексту з пробілами

h1_with_spaces = calculate_entropy(frequencies_with_spaces.values())
h2_no_overlap_with_spaces = calculate_entropy(bigram_counts_with_spaces.values()) / 2
h2_overlap_with_spaces = calculate_entropy(bigram_counts_overlap_with_spaces.values()) / 2

# Запис результатів в файл
with open("results_with_spaces.txt", "w", encoding="utf-8") as f:
    f.write("=== Результати для тексту з пробілами ===\n")
    f.write(f"Ентропія H1 (одиночні букви): {h1_with_spaces:.6f}\n")
    f.write(f"Ентропія H2 (біграми без перекриття): {h2_no_overlap_with_spaces:.6f}\n")
    f.write(f"Ентропія H2 (біграми з перекриттям): {h2_overlap_with_spaces:.6f}\n\n")

    f.write("=== Частоти букв ===\n")
    for letter, count in frequencies_with_spaces.items():
        freq = count / text_len
        f.write(f"'{letter}': {freq} \n")

    f.write("\n=== 5 найпоширеніших біграм з пробілами ===\n")
    for bigram, count in top_5_bigrams_with_spaces:
        f.write(f"'{bigram}': {count} \n")

# Створення таблиці біграм з пробілами
bmatrix_with_spaces = pd.DataFrame(0.0, index=sorted(frequencies_with_spaces.keys()), columns=sorted(frequencies_with_spaces.keys()))

sum_bigram_counts_overlap_with_spaces = sum(bigram_counts_overlap_with_spaces.values())
for bigram, freq in bigram_counts_overlap_with_spaces.items():
    bmatrix_with_spaces.at[bigram[0], bigram[1]] = freq / sum_bigram_counts_overlap_with_spaces

# Збереження таблиці біграм у CSV
bmatrix_with_spaces.to_csv('bmatrix_with_spaces.csv')

# Обробка тексту без пробілів
mytext_no_spaces = re.sub(r'[^а-яА-Я]', '', my_text).lower()

mytext_len_no_spaces = len(mytext_no_spaces)

# Частоти букв без пробілів
letter_frequencies_no_spaces = Counter(mytext_no_spaces)

# Підрахунок біграм без перекриття (без пробілів)
bigram_counts_no_overlap_no_spaces = defaultdict(int)
for i in range(0, mytext_len_no_spaces - 1, 2):
    bigram_counts_no_overlap_no_spaces[mytext_no_spaces[i:i+2]] += 1

# Підрахунок біграм з перекриттям (без пробілів)
bigram_counts_overlap_no_spaces = defaultdict(int)
for i in range(mytext_len_no_spaces - 1):
    bigram_counts_overlap_no_spaces[mytext_no_spaces[i:i+2]] += 1

# 5 найчастіших біграм без пробілів
top_5_bigrams_no_spaces = Counter(bigram_counts_overlap_no_spaces).most_common(5)

# Ентропія H1 та H2 для тексту без пробілів
h1_no_spaces = calculate_entropy(letter_frequencies_no_spaces.values())
h2_no_overlap_no_spaces = calculate_entropy(bigram_counts_no_overlap_no_spaces.values()) / 2
h2_overlap_no_spaces = calculate_entropy(bigram_counts_overlap_no_spaces.values()) / 2


# Запис результатів в файл
with open("results_no_spaces.txt", "w", encoding="utf-8") as f:
    f.write("=== Результати для тексту без пробілів ===\n")
    f.write(f"Ентропія H1 (одиночні букви): {h1_no_spaces:.6f}\n")
    f.write(f"Ентропія H2 (біграми без перекриття): {h2_no_overlap_no_spaces:.6f}\n")
    f.write(f"Ентропія H2 (біграми з перекриттям): {h2_overlap_no_spaces:.6f}\n\n")

    f.write("=== Частоти букв ===\n")
    for letter, count in letter_frequencies_no_spaces.items():
        freq = count / mytext_len_no_spaces
        f.write(f"'{letter}': {freq}\n")

    f.write("\n=== 5 найпоширеніших біграм без пробілів ===\n")
    for bigram, count in top_5_bigrams_no_spaces:
        f.write(f"'{bigram}': {count} \n")

# Створення таблиці біграм без пробілів
bmatrix_no_spaces = pd.DataFrame(0.0, index=sorted(letter_frequencies_no_spaces.keys()), columns=sorted(letter_frequencies_no_spaces.keys()))

total_sum_bigram_counts_overlap_no_spaces = sum(bigram_counts_overlap_no_spaces.values())
for bigram, freq in bigram_counts_overlap_no_spaces.items():
    bmatrix_no_spaces.at[bigram[0], bigram[1]] = freq / total_sum_bigram_counts_overlap_no_spaces

# Збереження таблиці біграм у CSV
bmatrix_no_spaces.to_csv('bmatrix_no_spaces.csv')
