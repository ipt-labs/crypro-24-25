from alphabet import Alphabet


class BigramAlphabet:

    def __init__(self, alphabet_string=""):
        self._alphabet = Alphabet(alphabet_string)
        self._m = len(alphabet_string)
        self._m2 = self._m * self._m

        self.bigrams_dict = dict()
        for i in range(self._m):
            letter1 = self._alphabet.get_letter(i)
            for j in range(self._m):
                bigram = letter1 + self._alphabet.get_letter(j)
                self.bigrams_dict[bigram] = i * self._m + j
        self.numbers_dict = dict(zip(self.bigrams_dict.values(), self.bigrams_dict.keys()))


    @property
    def m(self):
        return self._m

    @property
    def m2(self):
        return self._m2

    @property
    def alphabet(self):
        return self._alphabet

    def get_number(self, bigram):
        return self.bigrams_dict.get(bigram)

    def get_bigram(self, number):
        return self.numbers_dict.get(number)

    def get_numbers_list(self, bigrams_string):
        return [self.get_number(bigrams_string[i: i + 2])
                for i in range(0, len(bigrams_string), 2)]

    def get_bigrams_list(self, numbers):
        return [self.get_bigram(n) for n in numbers]

    def get_all_bigrams(self):
        return list(self.bigrams_dict.keys())