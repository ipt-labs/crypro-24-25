import math
import pandas as pd
from collections import Counter
from decimal import Decimal

class CryptoTextAnalyzator:
    def __init__(self, text, isSpace=False):
        if not text:
            raise ValueError("Не було надано текст!")

        self.isSpace = isSpace
        self.bigletter = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
        self.letter = self.bigletter.lower()

        # Фільтрація текстових даних і перетворення великих літер у малі
        valid_chars = str.maketrans('', '', ''.join(c for c in text if c not in self.bigletter + self.letter))
        self.text = text.translate(valid_chars).lower()

        if not isSpace:
            self.text = self.text.replace(' ', '')

        self.letter_freq_dict = self._compute_letter_freq()
        self.bigram_freq_overlap, self.bigram_freq_non_overlap = self._compute_bigram_freq()

    def _compute_letter_freq(self):
        letter_count = Counter(self.text)
        total_letters = len(self.text)
        return {k: v / total_letters for k, v in letter_count.items() if k in self.letter}

    def _compute_bigram_freq(self):
        n = len(self.text)
        bigram_count_overlap = Counter((self.text[i], self.text[i + 1]) for i in range(n - 1))
        bigram_count_non_overlap = Counter((self.text[i], self.text[i + 1]) for i in range(0, n - 1, 2)) #new
        total_overlap = sum(bigram_count_overlap.values())
        total_non_overlap = sum(bigram_count_non_overlap.values())

        bigram_freq_overlap = {bg: count / total_overlap for bg, count in bigram_count_overlap.items()}
        bigram_freq_non_overlap = {bg: count / total_non_overlap for bg, count in bigram_count_non_overlap.items()}

        return bigram_freq_overlap, bigram_freq_non_overlap

    def entropy(self, freq):
        return -sum(f * math.log2(f) for f in freq.values() if f > 0)

    def entropy_bigrams(self, bigram_freq):
        return self.entropy(bigram_freq) / 2  # Ділимо на 2

    def sourceRedundancy(self, entropy: Decimal, symbolsCount: int) -> Decimal:
        return Decimal(1) - (entropy / Decimal(math.log2(symbolsCount)))

    def save_to_excel(self, writer, sheet_suffix):
        df_letters = pd.DataFrame(list(self.letter_freq_dict.items()), columns=['Літеру', 'Частота'])
        df_letters.sort_values(by='Частота', ascending=False, inplace=True)  # Сортування за частотою

        bigram_matrix_overlap = self.create_bigram_matrix(self.bigram_freq_overlap)
        bigram_matrix_non_overlap = self.create_bigram_matrix(self.bigram_freq_non_overlap)

        df_letters.to_excel(writer, sheet_name=f'Літери {sheet_suffix}', index=False)
        bigram_matrix_overlap.to_excel(writer, sheet_name=f'Біграми_Перетин{sheet_suffix}')
        bigram_matrix_non_overlap.to_excel(writer, sheet_name=f'Біграмми_безП{sheet_suffix}')

    def create_bigram_matrix(self, bigram_freq):
        unique_letters = sorted(set(k[0] for k in bigram_freq.keys()).union(k[1] for k in bigram_freq.keys()))
        matrix = pd.DataFrame(0.0, index=unique_letters, columns=unique_letters)

        for (bg1, bg2), freq in bigram_freq.items():
            matrix.at[bg1, bg2] = round(freq, 3)

        return matrix

    def analyze(self):
        entropy_h1 = self.entropy(self.letter_freq_dict)
        symbols_count_h1 = len(self.letter_freq_dict)

        entropy_h2_overlap = self.entropy_bigrams(self.bigram_freq_overlap)
        entropy_h2_non_overlap = self.entropy_bigrams(self.bigram_freq_non_overlap)

        redundancy_h1 = self.sourceRedundancy(Decimal(entropy_h1), symbols_count_h1)
        redundancy_h2_overlap = self.sourceRedundancy(Decimal(entropy_h2_overlap), len(self.bigram_freq_overlap)) / 2  # Ділимо на 2
        redundancy_h2_non_overlap = self.sourceRedundancy(Decimal(entropy_h2_non_overlap), len(self.bigram_freq_non_overlap)) / 2  # Ділимо на 2

        return {
            "H1": round(entropy_h1, 5),
            "R1": round(redundancy_h1, 5),
            "H2_Перетин": round(entropy_h2_overlap, 5),
            "R2_Перетин": round(redundancy_h2_overlap, 5),
            "H2_Без_Перетин": round(entropy_h2_non_overlap, 5),
            "R2_Без_Перетин": round(redundancy_h2_non_overlap, 5)
        }

# Використання класу
with open('Chehov_Anton__A_P_Chehov_v_vospominaniyah_sovremennikov.txt', encoding='utf-8') as textfile:
    text = textfile.read()

analyzer_with_spaces = CryptoTextAnalyzator(text, isSpace=True)
analyzer_without_spaces = CryptoTextAnalyzator(text, isSpace=False)

summary_data = {
    "Метрика": ["H1", "R1", "H2_Перетин", "R2_Перетин", "H2_Без_Перетин", "R2_Без_Перетин"],
    "З Пробілами": [str(v).replace('.', ',') for v in analyzer_with_spaces.analyze().values()],
    "Без Пробілів": [str(v).replace('.', ',') for v in analyzer_without_spaces.analyze().values()],
}

summary_df = pd.DataFrame(summary_data)

with pd.ExcelWriter('crypto_analysis.xlsx') as writer:
    analyzer_with_spaces.save_to_excel(writer, sheet_suffix='(З Пробілами)')
    analyzer_without_spaces.save_to_excel(writer, sheet_suffix='(Без Пробілів)')
    summary_df.to_excel(writer, sheet_name='Зведена таблиця', index=False)

print("Аналіз завершено. Результати збережено у файлі 'crypto_analysis.xlsx'")
