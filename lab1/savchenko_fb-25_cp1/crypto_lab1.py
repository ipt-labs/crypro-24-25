import re
from collections import Counter, defaultdict
import math
import pandas as pd


def filter_text(text, no_space=False):
    text = re.sub(r'\s+', ' ', text).lower()
    
    if no_space:
        return re.sub(r'[^а-яА-Я]', '', text)

    return re.sub(r'[^а-яА-Я ]', '', text)

def letter_freq(text):
    freq = Counter(text)
    return freq

def bigrams_freq(text, overlp=False):
    step = 1
    if not overlp:
        step = 2

    bigram = defaultdict(int)
    for i in range(0, len(text) - 1, step):
        bigram[text[i:i+2]] += 1

    return bigram

def entropy(values):
    total = sum(values)
    return -sum((count / total) * math.log2(count / total) for count in values)

def calcBigrams(text, overlp=False, space=False):
    bigrams_dict = bigrams_freq(text, overlp)

    ALPHABET = ' абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    if not space:
        ALPHABET = ALPHABET[1:]
    
    bmatrix = pd.DataFrame(0.0, index=list(ALPHABET), columns=list(ALPHABET))
    values = bigrams_dict.values()
    sum_bigram = sum(values)
    alphabet_size = len(values)
    max_entropy = math.log2(alphabet_size) if alphabet_size > 0 else 0
    ev = entropy(values)

    redundancy = max_entropy - ev
    for letter1 in ALPHABET:
        for letter2 in ALPHABET:
            freq = bigrams_dict.get(letter1 + letter2, 0)
            bmatrix.at[letter1, letter2] = freq / sum_bigram
            
    return bmatrix, ev, redundancy

def calcForText(text, spaces=False):
    text_len = len(text)
    letters_freq_items = letter_freq(text)

    letters_freq = defaultdict(float)
    for letter, count in letters_freq_items.items():
        letters_freq[letter] = count / text_len

    bigrams_overlap, bigrams_overlap_entropy, r_overlap = calcBigrams(text, True, spaces)
    bigrams_no_overlap, bigrams_no_overlap_entropy, r_overlap_no = calcBigrams(text, False, spaces)

    bigrams_overlap_entropy_per_char = bigrams_overlap_entropy / 2
    bigrams_no_overlap_entropy_per_char = bigrams_no_overlap_entropy / 2

    bigrams_overlap.loc["Entropy"] = [str(bigrams_overlap_entropy)] + [""] * (len(bigrams_overlap.columns) - 1)
    bigrams_overlap.loc["R"] = [str(r_overlap)] + [""] * (len(bigrams_overlap.columns) - 1)

    bigrams_no_overlap.loc["Entropy"] = [str(bigrams_no_overlap_entropy)] + [""] * (len(bigrams_no_overlap.columns) - 1)
    bigrams_no_overlap.loc["R"] = [str(r_overlap_no)] + [""] * (len(bigrams_no_overlap.columns) - 1)

    letters_entropy = entropy(letters_freq_items.values())
    alphabet_size = len(letters_freq)
    max_entropy = math.log2(alphabet_size) if alphabet_size > 0 else 0
    redundancy = max_entropy - letters_entropy

    return (
        letters_freq,
        bigrams_overlap,
        bigrams_no_overlap,
        letters_entropy,
        redundancy,
        bigrams_overlap_entropy_per_char,
        bigrams_no_overlap_entropy_per_char
    )


def main():
    with open('/home/liza/fti/3curs/kripto/kriptok/lab1k/text.txt', "r", encoding="utf-8") as file:
        text = file.read()

    text_with_spaces = filter_text(text)
    text_wo_spaces = filter_text(text, True)

    letters_freq_spaces, bigrams_overlap_spaces, bigrams_no_overlap_spaces, letters_entropy_spaces, redundancy_spaces, bigrams_overlap_entropy_spaces, bigrams_no_overlap_entropy_spaces = calcForText(text_with_spaces, True)
    letters_freq_wo_spaces, bigrams_overlap_wo_spaces, bigrams_no_overlap_wo_spaces, letters_entropy_wo_spaces, redundancy_wo_spaces, bigrams_overlap_entropy_wo_spaces, bigrams_no_overlap_entropy_wo_spaces = calcForText(text_wo_spaces)

    letters_stats = "WITH SPACES:\n"
    for letter, freq in sorted(letters_freq_spaces.items(), key=lambda x: x[1], reverse=True):
        letters_stats += f"{letter}: {freq}\n"
    letters_stats += f"Entropy: {letters_entropy_spaces}\n"
    letters_stats += f"R: {redundancy_spaces}\n"
    letters_stats += f"Entropy bigrams (overlap) per char: {bigrams_overlap_entropy_spaces}\n"
    letters_stats += f"Entropy bigrams (no overlap) per char: {bigrams_no_overlap_entropy_spaces}\n"

    letters_stats += "\n\nWITHOUT SPACES:\n"
    for letter, freq in sorted(letters_freq_wo_spaces.items(), key=lambda x: x[1], reverse=True):
        letters_stats += f"{letter}: {freq}\n"
    letters_stats += f"Entropy: {letters_entropy_wo_spaces}\n"
    letters_stats += f"R: {redundancy_wo_spaces}\n"
    letters_stats += f"Entropy bigrams (overlap) per char: {bigrams_overlap_entropy_wo_spaces}\n"
    letters_stats += f"Entropy bigrams (no overlap) per char: {bigrams_no_overlap_entropy_wo_spaces}\n"

    bigrams_overlap_spaces.to_csv("bigrams_overlap_spaces.csv")
    bigrams_no_overlap_spaces.to_csv("bigrams_no_overlap_spaces.csv")
    bigrams_overlap_wo_spaces.to_csv("bigrams_overlap_wo_spaces.csv")
    bigrams_no_overlap_wo_spaces.to_csv("bigrams_no_overlap_wo_spaces.csv")

    with open('result_letters.txt', 'w', encoding='utf-8') as file:
        file.write(letters_stats)


if __name__ == "__main__":
    main()
