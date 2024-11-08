import math
import pandas as pd
from collections import Counter



def prep_text(path):
    file = open(path, "r", encoding="utf-8")
    text = file.read()
    text = text.lower()
    text = ''.join(filter(lambda char: char in set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"), text))
    text = text.replace('ъ', 'ь')
    text = text.replace('ё', 'е')
    return text



def main():
    text = prep_text()

if __name__ == "__main__":
    main()