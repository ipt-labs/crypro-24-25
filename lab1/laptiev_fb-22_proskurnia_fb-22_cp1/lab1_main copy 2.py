import math
import pandas as pd
from collections import Counter

class entrho_calc:

    def __init__(self, path, space=True):
        file = open(path, "r", encoding="utf-8")
        self.text = file.read()

        self.space = space
        self.text = self.text.lower()
        if (space==True):
            self.allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
        else:
            self.allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
        self.text = ''.join(filter(lambda char: char in self.allowed_chars, self.text))
        self.text = self.text.replace('ъ', 'ь')
        self.text = self.text.replace('ё', 'е')

        # monograms
        self.mono = pd.DataFrame.from_dict(Counter(self.text), orient='index', columns=['count']).reset_index().rename(columns={'index': 'char'})

        # bigrams overlapped
        self.bi_o = {}

        # bigrams not overlapped
        self.bi = {}


    # make matrix with frequancy
    def matrix_bi_freq(self, df, name):
        chars = sorted(self.allowed_chars)
        matrix = pd.DataFrame(0, index=chars, columns=chars)
        
        for _, row in df.iterrows():
            bigram = row['char']
            count = row['p']
            first_char, second_char = bigram
            matrix.at[first_char, second_char] = count
        matrix.to_csv(name+'.csv', encoding='utf-8')


    def enthropy(self, df, mono = False):
        ngram_len = len(df['char'].iloc[0])
        df['p'] = df['count'] / df['count'].sum()
        entropy = -sum(df['p'] * df['p'].apply(math.log2))/ngram_len

        if mono == True:
            df = df.sort_values(by='p', ascending=False)
            if self.space == True:
                df.to_csv('mono_freq_with_space.csv', encoding='utf-8')
            else:
                df.to_csv('mono_freq.csv', encoding='utf-8')

        return entropy

    # bigrams overlapped
    def bi_o_count(self):
        for i in range(len(self.text) - 1):
            bigram = self.text[i:i+2]
            if bigram in self.bi_o:
                self.bi_o[bigram] += 1
            else:
                self.bi_o[bigram] = 1
        self.bi_o = pd.DataFrame.from_dict(self.bi_o, orient='index', columns=['count']).reset_index().rename(columns={'index': 'char'})
        
        print('bigrams overlapped enthrophy:', self.enthropy(self.bi_o))

        if self.space == True:
            f_name = 'bi_o_space_freq_matrix'
        else:
            f_name = 'bi_o_freq_matrix'
        self.matrix_bi_freq(self.bi_o, f_name)

    # bigrams not overlapped
    def bi_count(self):
        for i in range(0, len(self.text) - 1, 2):
            bigram = self.text[i:i+2]
            if bigram in self.bi:
                self.bi[bigram] += 1
            else:
                self.bi[bigram] = 1
        self.bi = pd.DataFrame.from_dict(self.bi, orient='index', columns=['count']).reset_index().rename(columns={'index': 'char'})
        
        print('bigrams not overlapped enthrophy:', self.enthropy(self.bi))
        
        if self.space == True:
            f_name = 'bi_space_freq_matrix'
        else:
            f_name = 'bi_freq_matrix'
        self.matrix_bi_freq(self.bi, f_name)



def main():
    print('===== with space =====')
    text_with_space = entrho_calc("lab1/laptiev_fb-22_proskurnia_fb-22_cp1/text.txt")
    print('monograms enthrophy:', text_with_space.enthropy(text_with_space.mono, mono=True))
    text_with_space.bi_o_count()
    text_with_space.bi_count()

    print()

    print('===== without space =====')
    text_without_space = entrho_calc("lab1/laptiev_fb-22_proskurnia_fb-22_cp1/text.txt", False)
    print('monograms enthrophy:', text_without_space.enthropy(text_without_space.mono))
    text_without_space.bi_o_count()
    text_without_space.bi_count()
    pass

if __name__ == "__main__":
    main()