import os
import collections
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

class TextAnalyzer:
    # ініт та початкова обробка нашого тексту (майстер та маргарита)
    def __init__(self, text, script_dir):
        self.text = self.filter_text(text)
        self.text_no_spaces = self.remove_spaces(self.text)
        self.alphabet = ''.join(sorted(set(self.text)))
        self.alphabet_no_spaces = ''.join(sorted(set(self.text_no_spaces)))
        self.H_0_with_spaces = math.log2(len(self.alphabet))
        self.H_0_without_spaces = math.log2(len(self.alphabet_no_spaces))
        self.script_dir = script_dir
        self.output_dir = os.path.join(script_dir, 'output')
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def filter_text(text):
        text = text.lower()
        text = text.replace('ё', 'е').replace('ъ', 'ь')
        return ''.join(char for char in text if char.isalpha() or char == ' ')

    @staticmethod
    def remove_spaces(text):
        return text.replace(' ', '')
    
    # ф-ії для обчислення частот
    def calculate_frequencies(self, text):
        letter_freq = collections.Counter(text)
        total_chars = sum(letter_freq.values())
        letter_freq = {char: count / total_chars for char, count in letter_freq.items()}
        
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
        bigram_freq = collections.Counter(bigrams)
        total_bigrams = sum(bigram_freq.values())
        bigram_freq = {bigram: count / total_bigrams for bigram, count in bigram_freq.items()}
        
        non_overlapping_bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
        non_overlapping_bigram_freq = collections.Counter(non_overlapping_bigrams)
        total_non_overlapping_bigrams = sum(non_overlapping_bigram_freq.values())
        non_overlapping_bigram_freq = {bigram: count / total_non_overlapping_bigrams for bigram, count in non_overlapping_bigram_freq.items()}
        
        return letter_freq, bigram_freq, non_overlapping_bigram_freq, total_chars, total_bigrams

    @staticmethod
    def calculate_entropy(frequencies):
        return -sum(freq * math.log2(freq) for freq in frequencies.values() if freq > 0)

    def calculate_redundancy(self, H, with_spaces=True):
        if with_spaces:
            return 1 - (H / self.H_0_with_spaces)
        else:
            return 1 - (H / self.H_0_without_spaces)

    # ф-ії для виведення результатів
    def print_frequencies(self, frequencies, title):
        print(f"\n{title}:")
        sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
        for i, (item, freq) in enumerate(sorted_frequencies, 1):
            print(f"{item}: {freq:.10f}", end="  ")
            if i % 5 == 0:
                print()
        if len(sorted_frequencies) % 5 != 0:
            print()

    def print_bigram_frequencies(self, frequencies, title):
        print(f"\n{title}:")
        sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
        
        for i, (item, freq) in enumerate(sorted_frequencies[:5], 1):
            print(f"{item}: {freq:.10f}", end="  ")
        print("\n... ... ...")
        for i, (item, freq) in enumerate(sorted_frequencies[-5:], 1):
            print(f"{item}: {freq:.10f}", end="  ")
        print()

    # ф-ії матриць біграм
    def create_bigram_matrix(self, bigram_freq, alphabet):
        matrix = np.zeros((len(alphabet), len(alphabet)))
        for (c1, c2), freq in bigram_freq.items():
            if c1 in alphabet and c2 in alphabet:
                i, j = alphabet.index(c1), alphabet.index(c2)
                matrix[i, j] = freq
        return matrix

    def plot_bigram_matrix(self, matrix, alphabet, bigram_type, text_type):

        text_type = text_type.lower().replace(' ', '_')
        plt.figure(figsize=(12, 10))
        plt.imshow(matrix, cmap='viridis', norm=LogNorm())
        plt.colorbar(label='Частота (логарифмічна шкала)')
        plt.xticks(range(len(alphabet)), alphabet, rotation=90)
        plt.yticks(range(len(alphabet)), alphabet)
        plt.title(f"Біграми {(bigram_type.replace('_', ' '))} для тексту {text_type.replace('_', ' ')}")
        plt.xlabel('Друга буква біграми')
        plt.ylabel('Перша буква біграми')
        plt.tight_layout()
        
        directory = os.path.join(self.output_dir, 'біграм_матриці')
        os.makedirs(directory, exist_ok=True)
        
        filename = f"матриця_біграми_{bigram_type}_для_тексту_{text_type}.png"
        filepath = os.path.join(directory, filename)
        plt.savefig(filepath)
        plt.close()
        
        print(f"+] Файл {filename}")

    # ф-ії збережння
    def save_frequencies_to_excel(self, frequencies, filename, subfolder):
        directory = os.path.join(self.output_dir, subfolder)
        os.makedirs(directory, exist_ok=True)
        
        sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        df = pd.DataFrame(sorted_frequencies, columns=['Символ', 'Частота'])
        filepath = os.path.join(directory, filename)
        df.to_excel(filepath, index=False)
        print(f"+] Файл {filename}")

    def save_sorted_bigram_files(self, bigram_freq, alphabet, text_type):
        if "пробілів" in text_type:
            subfolder = 'без_пробілів'
        else:
            subfolder = 'з_пробілами'

        filename = f"сортовані_біграми_{text_type.lower().replace(' ', '_')}.xlsx"
        filepath = os.path.join(self.output_dir, subfolder, filename)

        bigrams_by_letter = {letter: [] for letter in alphabet}

        for letter in alphabet:
            letter_bigrams = [(bigram, freq) for bigram, freq in bigram_freq.items() if bigram.startswith(letter)]
            bigrams_by_letter[letter] = sorted(letter_bigrams, key=lambda x: x[1], reverse=True)

        max_bigrams = max(len(bigrams) for bigrams in bigrams_by_letter.values())

        headers = []
        for letter in alphabet:
            headers.append(f"{letter}")
            headers.append(f"Частота {letter}")

        content = []
        for i in range(max_bigrams):
            row = []
            for letter in alphabet:
                if i < len(bigrams_by_letter[letter]):
                    bigram, freq = bigrams_by_letter[letter][i]
                    row.append(bigram)
                    row.append(freq)
                else:
                    row.append("")
                    row.append("")
            content.append(row)

        df = pd.DataFrame([headers] + content)
        df.to_excel(filepath, index=False, header=False)
        print(f"+] Файл {filename}")

    def save_results_to_excel(self, results):
        filename = os.path.join(self.output_dir, "результати_аналізу.xlsx")
        
        rows = []
        for text_type, values in results.items():
            for parameter, value in values.items():
                rows.append({'Текст': text_type, 'Параметр': parameter, 'Значення': value})
        
        df = pd.DataFrame(rows)
        df.to_excel(filename, index=False)
        print(f"\n+] Результати аналізу збережено у файл: {filename}")

    def save_text_no_spaces_to_txt(self):
        filename = os.path.join(self.output_dir, 'text_no_spaces.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.text_no_spaces)
        print(f"+] Текст без пробілів збережено у файл: {filename}")


    # основна ф-ія аналізу
    def analyze(self):
        results = {}
        
        for text_type, text, alphabet in [("З пробілами", self.text, self.alphabet), 
                                        ("Без пробілів", self.text_no_spaces, self.alphabet_no_spaces)]:
            print(f"\n===== АНАЛІЗ ТЕКСТУ {text_type.upper()} =====")
            letter_freq, bigram_freq, non_overlapping_bigram_freq, total_chars, total_bigrams = self.calculate_frequencies(text)
            
            print(f"|] Загальна кількість символів: {total_chars}")
            print(f"||] Загальна кількість біграм: {total_bigrams}")
            
            self.print_frequencies(letter_freq, "[x] Частоти букв [x]")
            self.print_bigram_frequencies(bigram_freq, "[x/x] Біграми (перетинаючі) [x/x]")
            self.print_bigram_frequencies(non_overlapping_bigram_freq, "[x|x] Біграми (не перетинаючі) [x|x]")
            
            print("\n[SAVE] Збереження даних [SAVE]")
            subfolder = text_type.lower().replace(' ', '_')
            print(f"\nВ папку \"output\\{subfolder}\" збережено:")
            self.save_frequencies_to_excel(letter_freq, f"частоти_букв_{subfolder}.xlsx", subfolder)
            self.save_frequencies_to_excel(bigram_freq, f"частоти_біграм_перетинаючі_{subfolder}.xlsx", subfolder)
            self.save_frequencies_to_excel(non_overlapping_bigram_freq, f"частоти_біграм_не_перетинаючі_{subfolder}.xlsx", subfolder)
            
            self.save_sorted_bigram_files(bigram_freq, alphabet, f"перетинаючі_{text_type}")
            self.save_sorted_bigram_files(non_overlapping_bigram_freq, alphabet, f"не_перетинаючі_{text_type}")

            print("\nВ папку \"output\\біграм_матриці\" збережено:")
            matrix = self.create_bigram_matrix(bigram_freq, alphabet)
            self.plot_bigram_matrix(matrix, alphabet, "перетинаючі", text_type)
            
            matrix_non_overlapping = self.create_bigram_matrix(non_overlapping_bigram_freq, alphabet)
            self.plot_bigram_matrix(matrix_non_overlapping, alphabet, "не_перетинаючі", text_type)

            H_1 = self.calculate_entropy(letter_freq)
            H_2_overlapping = self.calculate_entropy(bigram_freq) / 2
            H_2_non_overlapping = self.calculate_entropy(non_overlapping_bigram_freq) / 2
            R_1 = self.calculate_redundancy(H_1, with_spaces=(text_type == "З пробілами"))
            R_2_overlapping = self.calculate_redundancy(H_2_overlapping, with_spaces=(text_type == "З пробілами"))
            R_2_non_overlapping = self.calculate_redundancy(H_2_non_overlapping, with_spaces=(text_type == "З пробілами"))

            
            results[text_type] = {
                "Ентропія H_1": H_1,
                "Ентропія H_2 (перетинаючі біграми)": H_2_overlapping,
                "Ентропія H_2 (не перетинаючі біграми)": H_2_non_overlapping,
                "Надлишковість R_1": R_1,
                "Надлишковість R_2 (перетинаючі біграми)": R_2_overlapping,
                "Надлишковість R_2 (не перетинаючі біграми)": R_2_non_overlapping,
            }
            print("\n")

        print("\n!=!=!=! РЕЗУЛЬТАТИ АНАЛІЗУ !=!=!=!")
        for text_type, values in results.items():
            print(f"\n[!] Результати аналізу для тексту {text_type.lower()} [!]:")
            for parameter, value in values.items():
                print(f"{parameter}: {value:.5f}")

        self.save_results_to_excel(results)
        self.save_text_no_spaces_to_txt()


# мейн
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    text_path = os.path.join(script_dir, 'text.txt')
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    analyzer = TextAnalyzer(text, script_dir)
    analyzer.analyze()

# запуск коду
if __name__ == "__main__":
    main()