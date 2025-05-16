from alphabet import Alphabet
from text_source_plus import TextSourcePlus
from ngram import NGrams
from vizhener_decipher import index_of_coincidence


def check_most_frequent_criteria(source: TextSourcePlus, alphabet: Alphabet,
                                 language_frequencies_sorted):
    f_quantity = 3
    ngrams = NGrams(alphabet, 1, source)
    ngrams.feed()
    source_frequencies = ngrams.get_ngrams_frequencies()
    # calculate sum of frequencies in text of 3 most frequent chars in language
    source_sum = 0
    for char in list(language_frequencies_sorted.keys())[: f_quantity]:
        source_sum += source_frequencies[char]
    # calculate sum of frequencies of 3 most frequent chars in language
    language_sum = sum(list(language_frequencies_sorted.values())[: f_quantity])
    print("check_most_frequent_criteria", language_sum, source_sum)
    sigma = (max(language_frequencies_sorted.values())
             - min(language_frequencies_sorted.values())) / 4   #(alphabet.m // f_quantity)
    return abs(source_sum - language_sum) <= sigma


def check_least_frequent_criteria(source: TextSourcePlus, alphabet: Alphabet,
                                  language_frequencies_sorted):
    f_quantity = 3
    ngrams = NGrams(alphabet, 1, source)
    ngrams.feed()
    source_frequencies = ngrams.get_ngrams_frequencies()
    source_sum = 0
    for char in list(language_frequencies_sorted.keys())[-f_quantity:]:
        source_sum += source_frequencies[char]
    language_sum = sum(list(language_frequencies_sorted.values())[-f_quantity:])
    print("check_least_frequent_criteria", language_sum, source_sum)
    sigma = (max(language_frequencies_sorted.values())
             - min(language_frequencies_sorted.values())) / 4   #(alphabet.m // f_quantity)
    return abs(source_sum - language_sum) <= sigma


def check_most_frequent_bigrams_criteria(source_cut: TextSourcePlus, alphabet: Alphabet,
                                         language_bigrams_frequencies_sorted):
    # have to delete first char of source text to check bigrams at intersections
    f_quantity = 3
    ngrams = NGrams(alphabet, 2, source_cut)
    ngrams.feed()
    source_frequencies = ngrams.get_ngrams_frequencies()
    source_sum = 0
    for bigram in list(language_bigrams_frequencies_sorted.keys())[: f_quantity]:
        source_sum += source_frequencies[bigram]
    language_sum = sum(list(language_bigrams_frequencies_sorted.values())[: f_quantity])
    print("check_most_frequent_bigrams_criteria", language_sum, source_sum)
    # m = alphabet.m ** 2
    sigma = (language_sum) / 4 #(m // f_quantity)
    return abs(source_sum - language_sum) <= sigma


def check_index_of_coincidence_criteria(source: TextSourcePlus,
                                        language_index_of_coincidence):
    ind = index_of_coincidence(source)
    print("check_index_of_coincidence_criteria", language_index_of_coincidence, ind)
    sigma = language_index_of_coincidence / 4
    return abs(language_index_of_coincidence - ind) <= sigma
