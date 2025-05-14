from text_source_plus import TextSourcePlus
from alphabet import Alphabet
from ngram import NGrams
from bigram_alphabet import BigramAlphabet
from bigram_affine_cipher import BigramAffineCipher, get_affine_keys_from_congruence
from detect_open_text import check_most_frequent_bigrams_criteria, check_most_frequent_criteria, \
    check_least_frequent_criteria, check_index_of_coincidence_criteria, index_of_coincidence

PATH_LAB1 = "..\\lab1\\"
LONG_FILE_NAME = "rus_text.txt"
PATH_LAB3 = "..\\lab3\\"
CIPHERED_FILE_NAME = "V10.txt"

RUS_LOWERCASE = "абвгдежзийклмнопрстуфхцчшщыьэюя"
MOST_FREQUENT_NUMBER = 5


def get_most_frequent(ngrams: NGrams, bigram_alphabet: BigramAlphabet, n):
    frequencies = ngrams.get_ngrams_frequencies(to_sort=True)
    numbers_list = [bigram_alphabet.get_number(bigram) for bigram in list(frequencies.keys())[: n]]
    bigrams_list = [bigram for bigram in list(frequencies.keys())[: n]]
    print(bigrams_list)
    return numbers_list


def gen_combinations(bigrams_most_frequent, language_most_frequent):
    for i, bigram in enumerate(bigrams_most_frequent):
        for j, language_bigram in enumerate(language_most_frequent):
            for i1 in range(i + 1, len(bigrams_most_frequent)):
                for j1 in range(j + 1, len(language_most_frequent)):
                    yield bigram, language_bigram, \
                          bigrams_most_frequent[i1], language_most_frequent[j1]


def is_likely_open_text(source: TextSourcePlus, alphabet,
                        language_frequencies_sorted,
                        language_bigrams_frequencies_sorted,
                        language_index_of_coincidence):
    source_cut = TextSourcePlus.from_string(source.filtered_as_string[1:], alphabet)
    source_cut.apply_filter_chain()
    criteria1 = check_most_frequent_criteria(source, alphabet, language_frequencies_sorted)
    criteria2 = check_least_frequent_criteria(source, alphabet, language_frequencies_sorted)
    criteria3 = check_most_frequent_bigrams_criteria(
        source_cut, alphabet, language_bigrams_frequencies_sorted)
    criteria4 = check_index_of_coincidence_criteria(source, language_index_of_coincidence)
    print(criteria1, criteria2, criteria3, criteria4)
    return criteria1 and criteria2 and criteria3 and criteria4


def decipher(source: TextSourcePlus, bigram_alphabet: BigramAlphabet,
             bigrams_most_frequent, language_most_frequent,
             language_frequencies_sorted,
             language_bigrams_frequencies_sorted,
             language_index_of_coincidence):
    # f = open("out.txt", "w", encoding='utf-8')
    alphabet = bigram_alphabet.alphabet
    for y1, x1, y2, x2 in gen_combinations(bigrams_most_frequent, language_most_frequent):
        a_b_list = get_affine_keys_from_congruence(y1, y2, x1, x2, bigram_alphabet.m2)
        if not a_b_list:
            continue

        print(a_b_list) #, file=f)
        for a, b in a_b_list:
            affine_bigram = BigramAffineCipher(a, b, bigram_alphabet)
            decipered = affine_bigram.decipher(source.filtered_as_string)
            if decipered is None:
                continue

            open_text_candidate = ''.join(decipered)
            print(f"a={a}, b={b}, text={open_text_candidate[:20]}") #, file=f)
            open_source_candidate = TextSourcePlus.from_string(open_text_candidate, alphabet)
            open_source_candidate.apply_filter_chain()
            if is_likely_open_text(open_source_candidate,
                                   alphabet,
                                   language_frequencies_sorted,
                                   language_bigrams_frequencies_sorted,
                                   language_index_of_coincidence):
                # f.close()
                return open_text_candidate
    # f.close()

# calculate characteristics of language using long russian text
alphabet = Alphabet(RUS_LOWERCASE)
bigram_alphabet = BigramAlphabet(RUS_LOWERCASE)
long_source = TextSourcePlus(PATH_LAB1 + LONG_FILE_NAME, alphabet, "to_lower", "replace_ru_yo_hard",
                             "delete_delimeters", "delete_spaces")
long_source.apply_filter_chain()
rus_index_of_coincidence = index_of_coincidence(long_source)
rus_unigrams = NGrams(alphabet, 1, long_source)
rus_unigrams.feed()
rus_bigrams = NGrams(alphabet, 2, long_source)
rus_bigrams.feed()
print(f"{MOST_FREQUENT_NUMBER} most frequent language bigrams for rus alphabet")
rus_bigrams_most_frequent = get_most_frequent(rus_bigrams, bigram_alphabet, MOST_FREQUENT_NUMBER)

# calculate characteristics of ciphered text
ciphered_source = TextSourcePlus(PATH_LAB3 + CIPHERED_FILE_NAME, alphabet)
ciphered_source.apply_filter_chain()
unigrams = NGrams(alphabet, 1, ciphered_source)
unigrams.feed()
bigrams = NGrams(alphabet, 2, ciphered_source)
bigrams.feed()
print(f"{MOST_FREQUENT_NUMBER}  most frequent bigrams for ciphered text")
bigrams_most_frequent = get_most_frequent(bigrams, bigram_alphabet, MOST_FREQUENT_NUMBER)

open_text = decipher(ciphered_source, bigram_alphabet,
                     bigrams_most_frequent, rus_bigrams_most_frequent,
                     rus_unigrams.get_ngrams_frequencies(to_sort=True),
                     rus_bigrams.get_ngrams_frequencies(to_sort=True),
                     rus_index_of_coincidence)

line_len = 60
print("\nIn the end of deciphering open text is:")
if open_text:
    for i in range(0, len(open_text), line_len):
        print(open_text[i: i + line_len])
