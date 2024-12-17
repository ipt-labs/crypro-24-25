import re
import pandas as pd
from collections import Counter, defaultdict
from math import log

def read_txt_file(path):
    with open(path, 'r', encoding='UTF-8') as file:
        text = file.read()
    return text

def clean_text(text):
    new_text = re.sub(r'[^а-яё ]', '', text.lower())
    new_text = re.sub(r'\s+', ' ', new_text)
    return new_text

def clean_text_no_spaces(text):
    new_text = re.sub(r'[^а-яё]', '', text.lower())
    return new_text

def get_bigrams(text):
    return [text[i:i+2] for i in range(len(text) - 1)]

def get_bigrams_no_overlap(text):
    return [text[i:i+2] for i in range(0, len(text) - 1, 2)]

def calc_char_frequencies(text, sort_by_value=False):
    count_map = Counter(text)
    char_total = len(text)
    frequencies = {char : count / char_total for char, count in count_map.items()}
    if sort_by_value:
        sorted_frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    else:
        sorted_frequencies = dict(sorted(frequencies.items()))
    return sorted_frequencies

def print_char_frequencies(char_frequencies):
    for key, value in char_frequencies.items():
        print(f"{value}")

def calc_bigram_frequencies(bigrams):
    bigrams_count = len(bigrams)
    count_matrix = defaultdict(lambda: defaultdict(int))

    for bigram in bigrams:
        first_char, second_char = bigram[0], bigram[1]
        count_matrix[first_char][second_char] +=1

    frequency_matrix = {}
    for first_char, inner_dict in count_matrix.items():
        frequency_matrix[first_char] = {second_char: count/bigrams_count for second_char, count in inner_dict.items()}
    return frequency_matrix

def print_bigram_frequency_matrix(frequency_matrix):
    sorted_matrix = dict(sorted(frequency_matrix.items()))
    all_columns = sorted({key for row in sorted_matrix.values() for key in row.keys()})
    
    max_width = max(len(f"{value:.5f}") for freq_list in sorted_matrix.values() for value in freq_list.values()) + 1
    header = ' ' * (max_width - 1) + ' '.join(f"{col:>{max_width}}" for col in all_columns)
    print(header)

    for char, freq_list in sorted_matrix.items():
        sorted_list = dict(sorted(freq_list.items()))  
        row = []
        for col in all_columns:
            row.append(f"{sorted_list.get(col, 0):>{max_width}.5f}")
        print(f"{char:>{max_width}} {' '.join(row)}")

def save_bigram_frequency_matrices_to_excel(file_name, matrices):
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:

        for sheet_name, matrix in matrices.items():
            pd.options.display.float_format = '{:,.8f}'.format  
            df = pd.DataFrame(matrix).fillna(0)  
            df = df.sort_index()  
            df = df.reindex(sorted(df.columns), axis=1)  
            df.to_excel(writer, sheet_name=sheet_name)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            for row in worksheet.iter_rows(min_row=2, min_col=2, max_row=worksheet.max_row, max_col=worksheet.max_column):
                for cell in row:
                    cell.number_format = '0.000000'  



def get_h1(probabilities):
    return -sum(p * log(p,2) for p in probabilities.values())

def get_h2(probabilities_matrix):
    h2 = 0.0
    for _, probabilities in probabilities_matrix.items():
        
        h2 += get_h1(probabilities)
    
    return h2/2

def get_redundancy(enthropy, alphabet_size):
    return 1 - (enthropy/log(alphabet_size, 2))

def do_lab1():
    text_path = 'alice.txt'

    raw_text = read_txt_file(text_path)
    text = clean_text(raw_text)
    text_no_spaces = clean_text_no_spaces(raw_text)
    
    print(text[:1000])
    
    print('\nLetter frequencies')

    print("\nwith spaces")
    char_frequencies = calc_char_frequencies(text, sort_by_value=True)
    print_char_frequencies(char_frequencies)

    print("\nwithout spaces")
    char_frequencies_no_spaces = calc_char_frequencies(text_no_spaces, sort_by_value=True)
    print_char_frequencies(char_frequencies_no_spaces)

    print('\nBigram frequencies')

    print('\nwith spaces, with overlap')
    frequency_matrix = calc_bigram_frequencies(get_bigrams(text))
    h2 = get_h2(frequency_matrix)
    print(f"H2: {h2}")
    print(f"R: {get_redundancy(h2, 34)}")
    print_bigram_frequency_matrix(frequency_matrix)
    
    print('\nno spaces, with overlap')
    frequency_matrix_no_spaces = calc_bigram_frequencies(get_bigrams(text_no_spaces))
    h2_no_spaces = get_h2(frequency_matrix_no_spaces)
    print(f"H2: {h2_no_spaces}")
    print(f"R: {get_redundancy(h2_no_spaces, 33)}")
    print_bigram_frequency_matrix(frequency_matrix_no_spaces)
    
    print('\nwith spaces, no overlap')
    frequency_matrix_no_overlaps = calc_bigram_frequencies(get_bigrams_no_overlap(text))
    h2_no_overlaps = get_h2(frequency_matrix_no_overlaps)
    print(f"H2: {h2_no_overlaps}")
    print(f"R: {get_redundancy(h2_no_overlaps, 34)}")
    print_bigram_frequency_matrix(frequency_matrix_no_overlaps)
    
    print('\nno spaces, no overlap')
    frequency_matrix_no_overlaps_no_spaces = calc_bigram_frequencies(get_bigrams_no_overlap(text_no_spaces))
    h2_no_overlaps_no_spaces = get_h2(frequency_matrix_no_overlaps_no_spaces)
    print(f"H2: {h2_no_overlaps_no_spaces}")
    print(f"R: {get_redundancy(h2_no_overlaps_no_spaces, 33)}")
    print_bigram_frequency_matrix(frequency_matrix_no_overlaps_no_spaces)

    print('\nH1\n')
    h1 = get_h1(char_frequencies)
    h1_no_spaces = get_h1(char_frequencies_no_spaces)
    print(f"regular: {h1}")
    print(f"no spaces: {h1_no_spaces}")

    print('\nR1\n')

    print(f"regular: {get_redundancy(h1, 34)}")
    print(f"no spaces: {get_redundancy(h1_no_spaces, 33)}\n")

    matrices_to_write = {
        'regular': frequency_matrix,
        'no overlaps':frequency_matrix_no_overlaps,
        'no spaces':frequency_matrix_no_spaces,
        'no spaces no overlaps':frequency_matrix_no_overlaps_no_spaces,
    }

    save_bigram_frequency_matrices_to_excel("aboba.xlsx", matrices_to_write)

do_lab1()