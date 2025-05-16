from copy import copy

from alphabet import Alphabet
from text_source import TextSource


class NGrams:

    def __init__(self, alphabet: Alphabet, length, source: TextSource):
        self._alphabet = alphabet
        self._length = length
        self._source = source
        self._ngrams = {ngram: 0 for ngram in self._construct_ngrams(self._length)}
        self._frequencies = {ngram: 0.0 for ngram in self._ngrams}
        self._errors = dict()

    def _construct_ngrams(self, n):
        if n == 0:
            return ['']

        ngrams = []
        for i in range(self._alphabet.m):
            letter = self._alphabet.get_letter(i)
            for gram in self._construct_ngrams(n - 1):
                ngrams.append(letter + gram)
        return ngrams

    def feed(self, intersected=False):
        step = 1 if intersected else self._length
        # calculate occurencies
        for i in range(0, self._source.size, step):
            text_ngram = ''.join(self._source.source_filtered[i: i + self._length])
            if text_ngram not in self._ngrams:
                self._errors[text_ngram] = self._errors.get(text_ngram, 0) + 1
                continue

            self._ngrams[text_ngram] += 1

        # calculate frequencies
        divisor = self._source.size // step
        if divisor == 0:
            return

        for ngram in self._ngrams:
            self._frequencies[ngram] = self._ngrams[ngram] / divisor

    def get_ngrams_quantities(self, to_sort=False):
        if not to_sort:
            return copy(self._ngrams)

        return dict(sorted(self._ngrams.items(), key=lambda item: item[1], reverse=True))

    def get_ngrams_frequencies(self, to_sort=False):
        if not to_sort:
            return copy(self._frequencies)

        return dict(sorted(self._frequencies.items(), key=lambda item: item[1], reverse=True))

    @property
    def errors(self):
        return self._errors
