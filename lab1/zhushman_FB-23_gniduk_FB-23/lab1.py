import re 
import collections
import pandas as pd
import math
import numpy as np
import chardet

with open("lab1.TXT", "rb") as file:
    result = chardet.detect(file.read())

#--- Очищення тексту від непотрібних символів ---
print("=== Виберіть режим обробки тексту ===")
print("1: Залишити пробіли")
print("2: Видалити пробіли")
user_input = input("Введіть номер обраного режиму (1 або 2): ")

with open("lab1.TXT", encoding=result['encoding'], errors="ignore") as f:
    file_content = f.read()

file_content = file_content.lower()
file_content = file_content.replace("\n", "")

if user_input == "1":
    cleaned_text = re.sub(r'[^\w\s]+|[\d]+|_+', '', file_content).strip()
    cleaned_text = re.sub(r'\s+', " ", cleaned_text)
elif user_input == "2":
    cleaned_text = re.sub(r'[\W\s]+|[\d]+|_+', '', file_content).strip()
else:
    print("Неправильний вибір. Завершення програми.")
    exit()

letters = list(cleaned_text)
print(cleaned_text)

#--- Кількість та частота появи літер ---

alphabet = letters.copy()

print("\n- Кількість літер у тексті -")
alphabet_dict = dict(collections.Counter(alphabet))

alphabet_dict = dict(sorted(alphabet_dict.items()))
print(alphabet_dict)

print("\n- Частота кожної літери в тексті -")
frequency = {k: alphabet_dict[k] / len(letters) for k in alphabet_dict}

frequency = dict(sorted(frequency.items()))
print(frequency)

#--- Виведення кількості літер у вигляді датафрейму ---

alphabet_filtered = sorted(alphabet_dict.keys())

letter_counts = [alphabet_dict[letter] for letter in alphabet_filtered]

df = pd.DataFrame({'Кількість у тексті': letter_counts}, index=alphabet_filtered)
df = df.rename(index={" ": "пробіл"})

#--- Виведення частоти літер ---

letter_frequencies = [frequency[letter] for letter in alphabet_filtered]

df2 = pd.DataFrame({'Частота': letter_frequencies}, index=alphabet_filtered)
df2 = df2.rename(index={" ": "пробіл"})

#--- Пошук біграм, підрахунок їх кількості та частоти ---

bigrams = [cleaned_text[i] + cleaned_text[i + 1] for i in range(len(cleaned_text) - 1)]
bigrams_non_overlapping = [cleaned_text[i] + cleaned_text[i + 1] for i in range(0, len(cleaned_text) - 1, 2)]

bigram_counts = dict(collections.Counter(bigrams))

bigram_frequencies = {k: bigram_counts[k] / len(bigrams) for k in bigram_counts}

bigram_non_overlapping_counts = dict(collections.Counter(bigrams_non_overlapping))
bigram_non_overlapping_frequencies = {k: bigram_non_overlapping_counts[k] / len(bigrams_non_overlapping) for k in bigram_non_overlapping_counts}

#--- Ентропія H1 ---

H1 = -sum(f * math.log2(f) for f in frequency.values())
print("\n- Ентропія:", H1, "-")  

#--- Питома ентропія H2 ---

def specific_entropy(bigram_frequencies):
    H2 = -sum(f * math.log2(f) for f in bigram_frequencies.values()) / 2
    return H2
  
H2_crossed = specific_entropy(bigram_frequencies) 
H2_non_overlapping = specific_entropy(bigram_non_overlapping_frequencies) 

print("- Питома ентропія на символ пересічної біграми:", H2_crossed, "-")
print("- Питома ентропія на символ непересічної біграми:", H2_non_overlapping, "-")

#--- Обчислення надлишковості ---

unique_letters = set(alphabet)
if ' ' in unique_letters:
    H0 = math.log2(len(unique_letters))  # Максимальна ентропія з пробілом
else:
    H0 = math.log2(len(unique_letters))  # Максимальна ентропія без пробілу

if ' ' in unique_letters:
    temp101 = H1
    temp201 = H2_crossed
    temp301 = H2_non_overlapping
    print("\n/// Надлишковість для тексту з пробілами ///")
else:
    temp102 = H1
    temp202 = H2_crossed
    temp302 = H2_non_overlapping
    print("\n/// Надлишковість для тексту без пробілів ///")

if ' ' in unique_letters:
    R1 = 1 - temp101 / H0
    R2_crossed = 1 - temp201 / H0
    R2_non_overlapping = 1 - temp301 / H0

    print(f"R1: {R1:.4f}")
    print(f"R2 для пересічних біграм: {R2_crossed:.4f}")
    print(f"R2 для непересічних біграм: {R2_non_overlapping:.4f}")
else:
    R1 = 1 - temp102 / H0
    R2_crossed = 1 - temp202 / H0
    R2_non_overlapping = 1 - temp302 / H0

    print(f"R1: {R1:.4f}")
    print(f"R2 для пересічних біграм: {R2_crossed:.4f}")
    print(f"R2 для непересічних біграм: {R2_non_overlapping:.4f}")

#--- Створення таблиць частоти біграм ---

alphabet_filtered = sorted(set(alphabet_filtered))
if ' ' in alphabet_filtered:
    alphabet_filtered[alphabet_filtered.index(' ')] = 'пробіл'

df3 = pd.DataFrame(index=alphabet_filtered, columns=alphabet_filtered, dtype=float)

for bigram, freq in bigram_frequencies.items():
    first_char, second_char = bigram[0], bigram[1]
    if first_char == ' ':
        first_char = 'пробіл'
    if second_char == ' ':
        second_char = 'пробіл'
    df3.at[first_char, second_char] = freq

df3 = df3.fillna(0)

print("\n- Таблиця частот пересічних біграм -")
print(df3)

df4 = pd.DataFrame(index=alphabet_filtered, columns=alphabet_filtered, dtype=float)

for bigram, freq in bigram_non_overlapping_frequencies.items():
    first_char, second_char = bigram[0], bigram[1]
    if first_char == ' ':
        first_char = 'пробіл'
    if second_char == ' ':
        second_char = 'пробіл'
    df4.at[first_char, second_char] = freq

df4 = df4.fillna(0)

print("\n- Таблиця частот непересічних біграм -")
print(df4)

if 'пробіл' in df.index:
    df.to_excel("Amount_with_space.xlsx")
    df3.to_excel("Bigram_Crossed_Frequency_with_space.xlsx")
    df4.to_excel("Bigram_Uncrossed_Frequency_with_space.xlsx")
else:
    df.to_excel("Amount_without_space.xlsx")
    df3.to_excel("Bigram_Crossed_Frequency_without_space.xlsx")
    df4.to_excel("Bigram_Uncrossed_Frequency_without_space.xlsx")
