import math

from alphabet import Alphabet
from text_source import TextSource
from ngram import NGrams


RUS_LOWERCASE = "абвгдежзийклмнопрстуфхцчшщьыэюя"
RUS_LOWERCASE_WITH_SPACE = RUS_LOWERCASE + ' '


def get_ngrams_entropy(frequencies, length):
    return -sum(frequencies[gram] * (math.log2(frequencies[gram]))
                for gram in frequencies if frequencies[gram] > 0) / length


def calculate_entropies(alphabet: Alphabet, source: TextSource, max_length=2):
    entropies = dict()
    intersected = False
    key = 1
    for length in range(1, max_length + 1):
        ngrams = NGrams(alphabet, length, source)
        ngrams.feed(intersected)
        entropies[key] = get_ngrams_entropy(ngrams.get_ngrams_frequencies(), length)
        key += 1

    # print(f"Errors: {ngrams.errors}")

    intersected = True
    key = 12
    for length in range(2, max_length + 1):
        ngrams = NGrams(alphabet, length, source)
        ngrams.feed(intersected)
        entropies[key] = get_ngrams_entropy(ngrams.get_ngrams_frequencies(), length)
        key += 1
    return entropies


def show_monogram_frequencies(alphabet: Alphabet, source: TextSource):
    ngrams = NGrams(alphabet, 1, source)
    ngrams.feed()
    frequencies = ngrams.get_ngrams_frequencies(to_sort=True)
    print("Monograms frequencies sorted")
    for letter, frequency in frequencies.items():
        print(f"'{letter}' {frequency:6.4f}")


def _build_axes_lists(bigrams_list):
    rows = list()
    cols = list()
    while bigrams_list:
        first, second = bigrams_list.pop(0)  # unpack bigram into 2 letters
        if first not in rows:
            rows.append(first)
        if second not in cols:
            cols.append(second)
    return rows, cols


def show_bigram_frequencies(alphabet: Alphabet, source: TextSource):
    ngrams = NGrams(alphabet, 2, source)
    ngrams.feed()
    frequencies = ngrams.get_ngrams_frequencies(to_sort=True)
    bigrams_list = list(frequencies.keys())
    # build lists of letters for rows and columns in sorted order
    rows, cols = _build_axes_lists(bigrams_list)

    print("Bigrams frequencies sorted")
    print("      " + "       ".join(cols))
    for i, first in enumerate(rows):
        f_string = f"{first} "
        for j, second in enumerate(cols):
            f_string += f" {frequencies[first + second]:7.5f}"
        print(f_string)


PATH_LAB1 = "..\\lab1\\"
LONG_FILE_NAME = "rus_text.txt"


alphabet = Alphabet(RUS_LOWERCASE_WITH_SPACE)
source = TextSource(PATH_LAB1 + LONG_FILE_NAME, alphabet, "to_lower", "replace_ru_yo_hard",
                    "replace_delimeters", "leave_one_space")
source.apply_filter_chain()

entropies = calculate_entropies(alphabet, source)
print("Entropies for 1 letter for source with space between words")
print(entropies)
h0 = math.log2(alphabet.m)
r = 1 - entropies[2] / h0
print(f"Excess of russian language in model with space approximately equals {r}")

alphabet = Alphabet(RUS_LOWERCASE)
source = TextSource(PATH_LAB1 + LONG_FILE_NAME, alphabet, "to_lower", "replace_ru_yo_hard",
                    "delete_delimeters", "delete_spaces")
source.apply_filter_chain()

print("\nFrequencies table for monograms for source without spaces")
show_monogram_frequencies(alphabet, source)

print("\nFrequencies table for bigrams for source without spaces")
show_bigram_frequencies(alphabet, source)

print("\nEntropies for 1 letter for source without spaces")
entropies = calculate_entropies(alphabet, source)
print(entropies)
h0 = math.log2(alphabet.m)
r = 1 - entropies[2] / h0
print(f"Excess of russian language in model without spaces approximately equals {r}")
