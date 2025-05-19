from random import randint

from alphabet import Alphabet
from text_source_plus import TextSourcePlus
from ngram import NGrams
from vizhener import VizhenerCipher


def index_of_coincidence(source: TextSourcePlus):
    if source.size <= 1:
        return 0

    ngrams = NGrams(source.alphabet, 1, source)
    ngrams.feed()
    s = 0
    for x in ngrams.get_ngrams_quantities().values():
        s += x * (x - 1)
    return s / (source.size * (source.size - 1))


def create_random_keyword(alphabet: Alphabet,  length):
    key_list = [alphabet.get_letter(randint(0, alphabet.m - 1)) for i in range(length)]
    return ''.join(key_list)


def cipher_source(source: TextSourcePlus, rmin, rmax):
    ciphered_dict = dict()
    keywords = list()
    for r in range(rmin, rmax + 1):
        keyword = create_random_keyword(source.alphabet, r)
        keywords.append(keyword)
        v = VizhenerCipher(keyword, source.alphabet)
        ciphered_dict[r] = ''.join(v.cipher(source.filtered_as_string))
    return keywords, ciphered_dict


class VizhenerDecipher:
    METHOD_1_R_MIN = 2
    METHOD_2_R_MIN = 6
    R_MAX = 30

    def __init__(self, source: TextSourcePlus, alphabet_co_index=1):
        self._source = source
        self._source.apply_filter_chain()
        self._alphabet_co_index = alphabet_co_index
        self._m = self._source.alphabet.m

    def get_index_of_coincidence_for_period(self, r):
        sources = TextSourcePlus.periodic(
            self._source.filtered_as_string, self._source.alphabet, r)
        for source in sources:
            source.apply_filter_chain()
        indexes = [ind for ind in map(index_of_coincidence, sources)]
        return sum(indexes) / len(indexes)  # average index of coincidence

    def periodic_method1_period_finder(self, return_all=False):
        uniform_index_of_coincidence = 1 / self._m
        sigma = abs(self._alphabet_co_index - uniform_index_of_coincidence) / 4
        candidate_periods = list()
        all_periods = list()
        for r in range(self.METHOD_1_R_MIN, self.R_MAX + 1):
            ind = self.get_index_of_coincidence_for_period(r)
            all_periods.append(
                (r, ind, self._alphabet_co_index, uniform_index_of_coincidence))
            if abs(ind - self._alphabet_co_index) <= sigma:
                candidate_periods.append(
                    (r, ind, self._alphabet_co_index, uniform_index_of_coincidence))
        return candidate_periods if not return_all else all_periods

    def non_periodic_method1_period_finder(self, ciphered_texts: dict, return_all=False):
        # ciphered_texts - dictionary of ciphered known text with key period as key
        # and text as value
        ciphered_indexes = dict()
        ind = index_of_coincidence(self._source)
        for r, ciphered in ciphered_texts.items():
            source = TextSourcePlus.from_string(ciphered, self._source.alphabet)
            source.apply_filter_chain()
            ciphered_indexes[r] = index_of_coincidence(source)
        sigma = (max(ciphered_indexes.values()) - min(ciphered_indexes.values())) / 6
        candidates = {r: idx for r, idx in ciphered_indexes.items() if abs(ind - idx) < sigma}
        return (ind, candidates) if not return_all else (ind, ciphered_indexes)

    def find_equals_num(self, source: TextSourcePlus):
        s = source.filtered_as_string
        return sum([1 if s[i] == s[i + 1] else 0 for i in range(len(s) - 1)])

    def stat_equals_method2_period_finder(self, return_all=False):
        stats = dict()
        for r in range(self.METHOD_2_R_MIN, self.R_MAX + 1):
            sources = TextSourcePlus.periodic(
                self._source.filtered_as_string, self._source.alphabet, r)
            d_n = 0
            for source in sources:
                source.apply_filter_chain()
                d_n += self.find_equals_num(source)
            stats[r] = d_n
        max_d_n = max(stats.values())
        sigma = (max_d_n - min(stats.values())) / 4
        candidates = {r: d_n for r, d_n in stats.items() if abs(max_d_n - d_n) < sigma}
        return candidates if not return_all else stats

    def detect_key_period(self):
        period_candidates = self.periodic_method1_period_finder()
        stats_candidates = self.stat_equals_method2_period_finder()
        r = 0
        if not period_candidates:
            return r

        potential_period = min(period_candidates)[0]
        min_stats_candidate = min(stats_candidates.keys())
        if min_stats_candidate % potential_period == 0:
            r = potential_period
        return r

    def _get_ith_most_frequent(self, ngrams: NGrams, i):
        frequencies = ngrams.get_ngrams_frequencies(to_sort=True)
        return list(frequencies.keys())[i]

    def _construct_keyword(self, sources, frequencies_numbers, language_ngrams):
        keyword = ""
        for j, source in enumerate(sources):
            ngrams = NGrams(source.alphabet, 1, source)
            ngrams.feed()
            y = self._get_ith_most_frequent(ngrams, 0)
            x = self._get_ith_most_frequent(language_ngrams, frequencies_numbers[j])
            number = (source.alphabet.get_number(y) - source.alphabet.get_number(x)
                      + source.alphabet.m) % source.alphabet.m
            keyword += source.alphabet.get_letter(number)
        return keyword

    def decipher(self, period, language_source: TextSourcePlus,
                 keyword="", frequencies_numbers=()):
        if not period:
            return "", ""

        if not keyword:
            language_ngrams = NGrams(self._source.alphabet, 1, language_source)
            language_ngrams.feed()

            sources = TextSourcePlus.periodic(
                self._source.filtered_as_string, self._source.alphabet, period)
            for source in sources:
                source.apply_filter_chain()
            keyword = self._construct_keyword(sources, frequencies_numbers, language_ngrams)
        vizhener = VizhenerCipher(keyword, self._source.alphabet)
        return keyword, vizhener.decipher(self._source.filtered_as_string)
