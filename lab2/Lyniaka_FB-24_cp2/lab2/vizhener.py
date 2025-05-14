from alphabet import Alphabet, ukr_alphabet


class VizhenerCipher:

    def __init__(self, keyword, alphabet: Alphabet):
        self._keyword = keyword
        self._alphabet = alphabet
        self._m = self._alphabet.m

    @property
    def keyword(self):
        return self._keyword

    def build_key(self, n):
        key = list(self._keyword) * (n // len(self._keyword) + 1)
        key = key[:n]
        return key

    def cipher(self, letters):
        key = self.build_key(len(letters))
        key_numbers = self._alphabet.get_numbers_list(key)
        numbers_list = [(x + y) % self._m
                        for x, y in zip(self._alphabet.get_numbers_list(letters),
                                        key_numbers)]
        return self._alphabet.get_letters_list(numbers_list)

    def decipher(self, ciphered_letters):
        key = self.build_key(len(ciphered_letters))
        key_numbers = self._alphabet.get_numbers_list(key)
        numbers_list = [(x + self._m - y) % self._m
                        for x, y in zip(self._alphabet.get_numbers_list(ciphered_letters),
                                        key_numbers)]
        return self._alphabet.get_letters_list(numbers_list)


MAX_KEYWORD_LEN = 10


def get_keyword_candidate(alphabet: Alphabet, open_letters, cipher_letters):
    open_numbers = alphabet.get_numbers_list(open_letters)
    open_numbers = open_numbers[:MAX_KEYWORD_LEN]
    cipher_numbers = alphabet.get_numbers_list(cipher_letters)
    cipher_numbers = cipher_numbers[:MAX_KEYWORD_LEN]
    keyword_numbers = [(y + alphabet.m - x) % alphabet.m for x, y in zip(open_numbers, cipher_numbers)]
    return alphabet.get_letters_list(keyword_numbers)


class VizhenerAutoKeyCipher(VizhenerCipher):

    def build_key(self, letters):
        key = list(self._keyword) + list(letters)
        key = key[:len(letters)]
        return key

    def cipher(self, letters):
        key = self.build_key(letters)
        key_numbers = self._alphabet.get_numbers_list(key)
        numbers_list = [(x + y) % self._m
                        for x, y in zip(self._alphabet.get_numbers_list(letters),
                                        key_numbers)]
        return self._alphabet.get_letters_list(numbers_list)

    def decipher(self, ciphered_letters):
        key = list(self._keyword)
        key_numbers = self._alphabet.get_numbers_list(key)
        numbers_list = list()
        for i, ch in enumerate(ciphered_letters):
            x = self._alphabet.get_number(ch)
            y = key_numbers[i]
            open_number = (x + self._m - y) % self._m
            numbers_list.append(open_number)
            # append new deciphered number and char to key
            if len(key) < len(ciphered_letters):
                key_numbers.append(open_number)
                key.append(self._alphabet.get_letter(open_number))
        return self._alphabet.get_letters_list(numbers_list)


class VizhenerCipheredAutoKeyCipher(VizhenerCipher):
    # ciphered text appended after keyword while ciphering
    def build_key(self, cipher_letters):
        key = list(self._keyword) + list(cipher_letters)
        key = key[:len(cipher_letters)]
        return key

    def cipher(self, letters):
        key = list(self._keyword)
        key_numbers = self._alphabet.get_numbers_list(key)
        numbers_list = list()
        for i, ch in enumerate(letters):
            x = self._alphabet.get_number(ch)
            y = key_numbers[i]
            cipher_number = (x + y) % self._m
            numbers_list.append(cipher_number)
            # append new deciphered number and char to key
            if len(key) < len(letters):
                key_numbers.append(cipher_number)
                key.append(self._alphabet.get_letter(cipher_number))
        return self._alphabet.get_letters_list(numbers_list)

    def decipher(self, cipher_letters):
        key = self.build_key(cipher_letters)
        key_numbers = self._alphabet.get_numbers_list(key)
        numbers_list = [(x + self._m - y) % self._m
                        for x, y in zip(self._alphabet.get_numbers_list(cipher_letters),
                                        key_numbers)]
        return self._alphabet.get_letters_list(numbers_list)


def get_open_candidate_for_added_ciphertext(alphabet: Alphabet, keylen, cipher_letters):
    keyword = [alphabet.get_letter(0)] * keylen
    cipher = VizhenerCipheredAutoKeyCipher(keyword, alphabet)
    return cipher.decipher(cipher_letters)


if __name__ == "__main__":
    # cipher = VizhenerCipher("САУРОН", ukr_alphabet)
    # ciphered_letters = cipher.cipher("ПЕРСТЕНЬНЕСЕФРОДО")
    # print(ciphered_letters)
    # print(cipher.decipher(ciphered_letters))

    print(get_keyword_candidate(ukr_alphabet, "СВІТЛОВИВМЕНЕАЛЕНЕПІЙМАВ", "ЬРРЇЬНІШІЕСМЛОФЩЯДШЩТЕЛБ"))
    print()

    cipher = VizhenerCipher("ЗОЗУЛЯ", ukr_alphabet)
    letters = cipher.decipher("ЬРРЇЬНІШІЕСМЛОФЩЯДШЩТЕЛБ")
    print(letters)
    print()

    # cipher = VizhenerAutoKeyCipher("САУРОН", ukr_alphabet)
    # ciphered_letters = cipher.cipher("ПЕРСТЕНЬНЕСЕФРОДО")
    # print(ciphered_letters)
    # print(cipher.decipher(ciphered_letters))
    # print()

    # cipher = VizhenerCipheredAutoKeyCipher("САУРОН", ukr_alphabet)
    # ciphered_letters = cipher.cipher("ПЕРСТЕНЬНЕСЕФРОДО")
    # print(ciphered_letters)
    # print(cipher.decipher(ciphered_letters))
    # print()

    # cipher_letters = "МГФЯВДЗИЯОЛЇАКНТ"
    # for keylen in range(1, 11):
    #     print(get_open_candidate_for_added_ciphertext(
    #         ukr_alphabet, keylen, cipher_letters))
    #
    # cipher = VizhenerCipheredAutoKeyCipher("КОЗАК", ukr_alphabet)
    # print()
    # print(cipher.decipher(cipher_letters))
