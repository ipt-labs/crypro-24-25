
UKR_CAPS = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
RUSSIAN_CAPS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
LATIN_CAPS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Alphabet:

    def __init__(self, alphabet_string=""):
        self.letters_dict = {c: i for i, c in enumerate(alphabet_string)}
        self.numbers_dict = dict(zip(self.letters_dict.values(), self.letters_dict.keys()))

        self._m = len(alphabet_string)

    @property
    def m(self):
        return self._m

    def get_number(self, letter):
        return self.letters_dict.get(letter)

    def get_letter(self, number):
        return self.numbers_dict.get(number)

    def get_numbers_list(self, letters):
        return [self.get_number(c) for c in letters]

    def get_letters_list(self, numbers):
        return [self.get_letter(n) for n in numbers]

    def get_all_letters(self):
        return list(self.letters_dict.keys())


latin_alfabet = Alphabet(LATIN_CAPS)
ukr_alphabet = Alphabet(UKR_CAPS)
rus_alphabet = Alphabet(RUSSIAN_CAPS)
