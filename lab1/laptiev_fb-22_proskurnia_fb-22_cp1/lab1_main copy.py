import math
import csv
from decimal import *

class entrho_calc:
    def __init__(self, path, space=True):
        file = open(path, "r", encoding="utf-8")
        self.text = file.read()

        self.text = self.text.lower()
        if (space==True):
            self.allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
        else:
            self.allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
        self.text = ''.join(filter(lambda char: char in self.allowed_chars, self.text))
        self.text = self.text.replace('ъ', 'ь')
        self.text = self.text.replace('ё', 'е')

        self.monogram_count = 0
        self.monograms = {}

        self.bigram_count = 0
        self.bigrams = {}

        self.totalOverlappedBigrams = 0
        self.overlappedBigramCount = {}

    def save_to_file(self, name=""):
        with open("normalized_text" + name + ".txt", "w", encoding="utf-8") as file:
            file.write(self.text)
            file.close()

    def count_monograms(self):
        for char in self.text:
            if char in self.monograms:
                self.monograms[char] += 1
            else:
                self.monograms[char] = 1
            self.monogram_count += 1
    
    def count_bigrams(self):
        self.bigrams={}
        for i in range(len(self.text) - 1):
            bigram = self.text[i:i+2]
            if bigram in self.bigrams:
                self.bigrams[bigram] += 1
            else:
                self.bigrams[bigram] = 1
            self.bigram_count += 1

    def count_bigrams_not_overlapped(self):
        self.bigrams={}
        for i in range(0, len(self.text) - 1, 2):
            bigram = self.text[i:i+2]
            if bigram in self.bigrams:
                self.bigrams[bigram] += 1
            else:
                self.bigrams[bigram] = 1
            self.bigram_count += 1

    def mono_frequancy_calc(self):
        for char in self.monograms:
                self.monograms[char] = self.monograms[char] / self.monogram_count

    def bigr_frequancy_calc(self):
        for char in self.bigrams:
                self.bigrams[char] = self.bigrams[char] / self.bigram_count

    # def entrophy_calc(self, freq_list):
    #     entrophy = Decimal(0)
    #     for freq in freq_list.values():
    #         freq = Decimal(freq)
    #         if not freq.is_zero():
    #             entrophy -= freq * Decimal(math.log2(freq))
    #     return entrophy/len(list(freq_list.keys())[0])

    def entrophy_calc(self, freq_list):
        for char in freq_list:
                freq_list[char] = freq_list[char] * math.log2(freq_list[char])
        return -sum(freq_list.values())
    
    def bigram_frequency_matrix(self):
        alphabet = ''.join(self.allowed_chars)
        matrix = [[0 for _ in range(len(alphabet))] for _ in range(len(alphabet))]

        for bigram, freq in self.bigrams.items():
            row = alphabet.index(bigram[0])
            col = alphabet.index(bigram[1])
            matrix[row][col] = freq

        return matrix

    def save_matrix_to_csv(self, matrix, filename):
        alphabet = ''.join(self.allowed_chars)
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header
            writer.writerow([''] + list(alphabet))
            # Write the matrix rows
            for i, row in enumerate(matrix):
                writer.writerow([alphabet[i]] + row)

def main():
    print("######-spaces-######")
    # text_with_space = entrho_calc("text.txt")
    text_with_space = entrho_calc("lab1/laptiev_fb-22_proskurnia_fb-22_cp1/text.txt")

    #monograms
    text_with_space.count_monograms()
    text_with_space.mono_frequancy_calc()
    # print("monograms frequancy:")
    # for char, gram in text_with_space.monograms.items():
    #     print(f"{char}, {gram:.20f}")
    print(f"monograms entrophy: {text_with_space.entrophy_calc(text_with_space.monograms)}")

    #birgams overlapped
    text_with_space.count_bigrams()
    text_with_space.bigr_frequancy_calc()
    # print("bigrams frequancy:")
    # for char, gram in text_with_space.bigrams.items():
    #     print(f"{char}, {gram:.20f}")
    print(f"bigrams overlapped entrophy: {text_with_space.entrophy_calc(text_with_space.bigrams)}")

    # matrix = text_with_space.bigram_frequency_matrix()
    # text_with_space.save_matrix_to_csv(matrix, 'bigram_frequency_overlapped_with_space_matrix.csv')

    #birgams not overlapped
    text_with_space.count_bigrams_not_overlapped()
    text_with_space.bigr_frequancy_calc()
    # print("bigrams frequancy:")
    # for char, gram in text_with_space.bigrams.items():
    #     print(f"{char}, {gram:.20f}")
    print(f"bigrams not overlapped entrophy: {text_with_space.entrophy_calc(text_with_space.bigrams)}")

    # matrix = text_with_space.bigram_frequency_matrix()
    # text_with_space.save_matrix_to_csv(matrix, 'bigram_frequency_with_space_matrix.csv')

#===============================================================================================================================

    print("\n######-NO spaces-######")
    # text_without_space = entrho_calc("text.txt", False)
    text_without_space = entrho_calc("lab1/laptiev_fb-22_proskurnia_fb-22_cp1/text.txt", False)
    # text_without_space.save_to_file("_another_file")

    #monograms
    text_without_space.count_monograms()
    text_without_space.mono_frequancy_calc()
    # print("monograms frequancy:")
    # for char, gram in text_without_space.monograms.items():
    #     print(f"{char}, {gram:.20f}")
    print(f"monograms entrophy: {text_without_space.entrophy_calc(text_without_space.monograms)}")

    #bigrams overlapped
    text_without_space.count_bigrams()
    text_without_space.bigr_frequancy_calc()
    # print("bigrams frequancy:")
    # for char, gram in text_without_space.bigrams.items():
    #     print(f"{char}, {gram:.20f}")
    print(f"bigrams overllaped entrophy: {text_without_space.entrophy_calc(text_without_space.bigrams)}")
    
    # matrix = text_without_space.bigram_frequency_matrix()
    # text_without_space.save_matrix_to_csv(matrix, 'bigram_frequency_without_space_overlapped_matrix.csv')

    #bigrams not overlapped
    text_without_space.count_bigrams_not_overlapped()
    text_without_space.bigr_frequancy_calc()
    # print("bigrams frequancy:")
    # for char, gram in text_without_space.bigrams.items():
    #     print(f"{char}, {gram:.20f}")
    print(f"bigrams not overllaped entrophy: {text_without_space.entrophy_calc(text_without_space.bigrams)}")

    # matrix = text_without_space.bigram_frequency_matrix()
    # text_without_space.save_matrix_to_csv(matrix, 'bigram_frequency_without_space_matrix.csv')


if __name__ == "__main__":
    main()