import re
import os
import pandas as pd
from math import log
from collections import Counter


# форматуємо текст, прибираємо зайві пробіли, робимо букви з маленької
def text_format(text, spaces):
    text = text.lower()
    text = re.sub(r'[^а-яё ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if not spaces:
        text = text.replace(' ', '')
    return text


# розрахунок частоти
def frequency(sum, total):
    freq = {}
    for value in sum:
        freq[value] = sum[value] / total

    return freq


# рахуємо ентропію
def enthropy(freq):
    temp = []
    for i in freq.values():
        temp.append(i * log(i, 2))

    H = -sum(temp)
    return H


def redundance(H, alphabet):
    # обчислення надлишковості
    result = 1 - (H/log(len(alphabet), 2)) 
    return result


# робимо датафрейм для біграм та монограм, 
# який містить  скільки разів попадалася певна біграма або монограма та їх частоту
def make_dataframe(name, spaces, total=0, counts=0):
    df = pd.DataFrame(list(counts.items()), columns=[name, 'Count'])

    df['Frequency'] = df['Count'] / total
    df_sorted = df.sort_values(by='Count', ascending=False)

    if spaces:
        df_sorted.to_excel(f'{name}s_with_spaces.xlsx', index=False)
    else:
         df_sorted.to_excel(f'{name}s_without_spaces.xlsx', index=False)
   
    return df_sorted


# ф-ія для побудови таблиці частот для біграм
def build_matrix(alphabet, bigram_counts, total_bigrams, name, spaces):
    bigram_matrix = pd.DataFrame(0.0, index=list(alphabet), columns=list(alphabet))
    
    for bigram, count in bigram_counts.items():
        first_letter, second_letter = bigram
        bigram_matrix.at[first_letter, second_letter] = count / total_bigrams  

    bigram_matrix = bigram_matrix.fillna(0)

    if spaces:
        bigram_matrix.to_excel(f'{name}_with_spaces.xlsx', index=True)
    else:
        bigram_matrix.to_excel(f'{name}_without_spaces.xlsx', index=True)

    return bigram_matrix


# розрахунок кількості монограм, їхньої частоти, ентропії та надлишковості
# побудова датафрейму з даними
def monograms(text, alphabet, spaces):
    monogram_counts = Counter(text)
    total_letters = sum(monogram_counts.values())

    freq = frequency(monogram_counts, total_letters)
    H1 = enthropy(freq) 
    redundance_res = redundance(H1, alphabet)

    df = make_dataframe('Monogram',spaces, total_letters, monogram_counts)

    return freq, H1, redundance_res, df


# аналогічні дії виконуємо з біграмами, так як і з монограмами попередньо
def bigrams(text, alphabet, spaces):
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_counts = Counter(bigrams)
    total_bigrams = len(text) 

    freq = frequency(bigram_counts, total_bigrams)
    H2 = enthropy(freq) / 2
    redundance_res = redundance(H2, alphabet)

    df = make_dataframe('Bigram', spaces, total_bigrams, bigram_counts)
    matrix = build_matrix(alphabet, bigram_counts, total_bigrams, 'bigram_matrix', spaces)

    return freq, H2, redundance_res, df, matrix


# аналогічно з біграмами з кроком 2
def bigrams_with_step_2(text, alphabet, spaces):
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    bigram_counts = Counter(bigrams)
    total_bigrams = len(bigrams)

    freq = frequency(bigram_counts, total_bigrams)
    H2 = enthropy(freq) / 2
    redundance_res = redundance(H2, alphabet)

    df = make_dataframe('Step2_Bigram', spaces, total_bigrams, bigram_counts)
    matrix = build_matrix(alphabet, bigram_counts, total_bigrams, 'bigram_matrix_step2', spaces)

    return freq, H2, redundance_res, df, matrix


def main(initial_text, spaces):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
    
    with open(initial_text, 'r') as file:
        initial_text = file.read()

    edited_text = text_format(initial_text, spaces)
    monograms_res = monograms(edited_text, alphabet, spaces)
    bigrams_res = bigrams(edited_text, alphabet, spaces)
    bigrams_with_step_2_res = bigrams_with_step_2(edited_text, alphabet, spaces)

    print(f''' 
        Monograms:
          - enthropy: {monograms_res[1]}
          - redundance: {monograms_res[2]}

        Bigrams:
          - enthropy: {bigrams_res[1]}
          - redundance: {bigrams_res[2]}

        Bigrams_with_step_2:
          - enthropy: {bigrams_with_step_2_res[1]}
          - redundance: {bigrams_with_step_2_res[2]}
    ''')


main(os.environ.get('FILE'), False)
