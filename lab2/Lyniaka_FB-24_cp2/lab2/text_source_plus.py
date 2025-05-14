from alphabet import Alphabet
from text_source import TextSource


class TextSourcePlus(TextSource):

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def filtered_as_string(self):
        return ''.join(self._source_filtered)

    @classmethod
    def from_string(cls, source_string, alphabet: Alphabet, *filters):
        source = cls(None, alphabet, *filters)
        source._start_source = source_string
        return source

    @classmethod
    def periodic(cls, source_string, alphabet: Alphabet, r, *filters):
        sources = list()
        for i in range(r):
            periodic_list = [source_string[j] for j in range(i, len(source_string), r)]
            periodic_string = ''.join(periodic_list)
            sources.append(cls.from_string(periodic_string, alphabet, *filters))
        return sources

    @staticmethod
    def replace_ru_yo_filter(source: str, to_replace=(('ё', 'е'), )):
        to_replace_dict = dict(to_replace)
        filtered = [c if c not in to_replace_dict else to_replace_dict[c] for c in source]
        return ''.join(filtered)
