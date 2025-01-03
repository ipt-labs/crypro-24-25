import pandas as pd

def find_top_5_bigrams(file_path):
    matrix = pd.read_csv(file_path, index_col=0)

    bigram_values = []
    for row_char in matrix.index:
        for col_char in matrix.columns:
            value = matrix.at[row_char, col_char]
            if value > 0:  
                bigram_values.append((f"{row_char}{col_char}", value))
    bigram_values = sorted(bigram_values, key=lambda x: x[1], reverse=True)
    return bigram_values[:5]

file_paths = ['bi_freq_matrix.csv']

for file_path in file_paths:
    print(f"Top 5 bigrams in {file_path}:")
    top_bigrams = find_top_5_bigrams(file_path)
    for bigram, value in top_bigrams:
        print(f"{bigram}: {value}")
    print()
