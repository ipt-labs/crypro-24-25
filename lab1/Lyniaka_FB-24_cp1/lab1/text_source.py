from alphabet import Alphabet, ukr_alphabet

STANDARD_DELIMETERS = '.,:;()"\'0123456789+-_№#&!?/|\\%$«»*—„“–…=[]{}'


class TextSource:

    def __init__(self, file_path=None, alphabet: Alphabet = ukr_alphabet, *filters):
        self._alphabet = alphabet
        self._start_source = ""
        if file_path is not None:
            with open(file_path, 'r', encoding="utf-8") as f:
                self._start_source: str = f.read()
        self._filter_chain = list()
        self._source_filtered = list()
        for filter_name in filters:
            self.add_filter(filter_name)

    def add_filter(self, filter_name):
        filt = getattr(self, filter_name + "_filter", None)
        if filt is None:
            return False

        self._filter_chain.append(filt)
        return True

    def apply_filter_chain(self):
        source = self._start_source
        for filt in self._filter_chain:
            source = filt(source)
        self._source_filtered = self.delete_non_alphabet_letters(source)

    @property
    def source_filtered(self):
        return self._source_filtered

    @property
    def size(self):
        return len(self._source_filtered)

    @staticmethod
    def to_lower_filter(source: str):
        return source.lower()

    @staticmethod
    def to_upper_filter(source: str):
        return source.upper()

    @staticmethod
    def leave_one_space_filter(source: str):
        return ' '.join(source.split())

    @staticmethod
    def delete_spaces_filter(source: str):
        return ''.join(source.split())

    @staticmethod
    def delete_delimeters_filter(source: str, delim=STANDARD_DELIMETERS):
        delimeters = set(delim)
        filtered = [c if c not in delimeters else "" for c in source]
        return ''.join(filtered)

    @staticmethod
    def replace_delimeters_filter(source: str, delim=STANDARD_DELIMETERS):
        delimeters = set(delim)
        filtered = [c if c not in delimeters else ' ' for c in source]
        return ''.join(filtered)

    @staticmethod
    def replace_ru_yo_hard_filter(source: str, to_replace=(('ё', 'е'), ('ъ', 'ь'))):
        to_replace_dict = dict(to_replace)
        filtered = [c if c not in to_replace_dict else to_replace_dict[c] for c in source]
        return ''.join(filtered)

    def delete_non_alphabet_letters(self, source: str):
        alphabet_letters = set(self._alphabet.get_all_letters())
        return [c for c in source if c in alphabet_letters]
