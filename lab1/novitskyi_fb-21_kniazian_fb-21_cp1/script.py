import re
from collections import Counter
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

LETTERS = "абвгдежзийклмнопрстуфхцчшщыьэюя "
LETTERS_WITHOUT_SPACE = "абвгдежзийклмнопрстуфхцчшщыьэюя"
FILE_PATH = "D:/3/crypto/Tolkien.txt"

def filter_text(text, space=False):
    text = text.lower()
    text = text.replace("ё", "е")
    text = text.replace("ъ", "ь")
    text = re.sub("[^а-я]", " ", text)
    if space:
        text = re.sub(r"\s+", " ", text)
    else:
        text = re.sub(r"\s+", "", text)
    return text


def entropy_(frequency_list):
    entropy = 0
    for frequency in frequency_list:
        entropy += frequency * math.log2(frequency)
    return -entropy


def letter_frequency_entropy(text, space=False):
    frequency_dict = {}
    letters_amount = len(text)
    if space:
        for letter in LETTERS:
            frequency = text.count(letter) / letters_amount
            frequency_dict[letter] = frequency
        print("Частота появи букв з пробілами:")
    else:
        for letter in LETTERS_WITHOUT_SPACE:
            frequency = text.count(letter) / letters_amount
            frequency_dict[letter] = frequency
        print("Частота появи букв без пробілів:")
    sorted_frequency_list = sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)
    for letter, frequency in sorted_frequency_list:
        print(f"{letter}: {frequency:.7f}, {frequency*100:.2f}%")
    entropy = entropy_(frequency_dict.values())
    print("\nПитома ентропія на символ:")
    print(f"H1 = {entropy:.2f}")
    print()


def plot_bigram_heatmap(frequency_dict, space=False):
    if space:
        letters = LETTERS
    else:
        letters = LETTERS_WITHOUT_SPACE
    matrix_size = len(letters)
    matrix = np.zeros((matrix_size, matrix_size))
    for bigram, frequency in frequency_dict.items():
        i = letters.index(bigram[0])
        j = letters.index(bigram[1])
        matrix[i, j] = frequency
    df = pd.DataFrame(matrix, index=list(letters), columns=list(letters))
    plt.figure(figsize=(12, 10))
    sns.heatmap(df, cmap="inferno", mask=df == 0)
    plt.title("Частоти біграм")
    plt.xlabel("Друга літера біграми")
    plt.ylabel("Перша літера біграми")
    plt.show()


def bigram_frequency_entropy(text, space=False):
    frequency_dict = {}
    bigrams = []
    for step in [1, 2]:
        for i in range(0, len(text) - 1, step):
            bigram = text[i : i + 2]
            bigrams.append(bigram)
        bigram_dict = Counter(bigrams)
        bigrams_amount = sum(bigram_dict.values())
        for bigram in bigram_dict:
            frequency = bigram_dict[bigram] / bigrams_amount
            frequency_dict[bigram] = frequency
        top_frequency_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)[:10])
        if space:
            print(f"Частота появи 10 найчастіших біграм з кроком {step} з пробілами:")
        else:
            print(f"Частота появи 10 найчастіших біграм з кроком {step} без пробілів:")
        for bigram in top_frequency_dict:
            print(f"{bigram}: {top_frequency_dict[bigram]:.7f}, {top_frequency_dict[bigram]*100:.2f}%")
        entropy = entropy_(frequency_dict.values()) / 2
        print("\nПитома ентропія на символ:")
        print(f"H2 = {entropy:.2f}")
        print()
        plot_bigram_heatmap(frequency_dict, space)
        

def main():
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        content = file.read()
    
    content = filter_text(content, True)
    content_without_space = filter_text(content)
    letter_frequency_entropy(content, True)
    letter_frequency_entropy(content_without_space)
    bigram_frequency_entropy(content, True)
    bigram_frequency_entropy(content_without_space)


if __name__ == "__main__":
    main()