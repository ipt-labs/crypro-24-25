#!/bin/python
from typing import Callable
from math import log2
from decimal import *

import pandas as pd
import argparse
import pprint
import os

# Precision for Decimal.
getcontext().prec = 50

# 1 << 16 = 64KB.
TEXT_BLOCK_SIZE = 1 << 16
NULL = "\x00"

STANDARD_ALPHABET = {
    "А": "а", "Б": "б", "В": "в", "Г": "г", "Д": "д", "Е": "е", "Ж": "ж", "З": "з", "И": "и", "Й": "й", "К": "к",
    "Л": "л", "М": "м", "Н": "н", "О": "о", "П": "п", "Р": "р", "С": "с", "Т": "т", "У": "у", "Ф": "ф", "Х": "х",
    "Ц": "ц", "Ч": "ч", "Ш": "ш", "Щ": "щ", "Ъ": "ъ", "Ы": "ы", "Ь": "ь", "Э": "э", "Ю": "ю", "Я": "я"
}

STANDARD_ALPHABET_WHITESPACE = {
    "А": "а", "Б": "б", "В": "в", "Г": "г", "Д": "д", "Е": "е", "Ж": "ж", "З": "з", "И": "и", "Й": "й", "К": "к",
    "Л": "л", "М": "м", "Н": "н", "О": "о", "П": "п", "Р": "р", "С": "с", "Т": "т", "У": "у", "Ф": "ф", "Х": "х",
    "Ц": "ц", "Ч": "ч", "Ш": "ш", "Щ": "щ", "Ъ": "ъ", "Ы": "ы", "Ь": "ь", "Э": "э", "Ю": "ю", "Я": "я", "\x00": " "
}

STATICTIC_OUTPUT_FILE = "statistics"
STATICTIC_OUTPUT_FILE_WHITESPACED = "statistics_whitespaced"
EXCEL_EXTENSION = ".xlsx"
CSV_EXTENSION = ".csv"

class EntropyCalculator:
    alphabet: set
    up2low: dict[str, str]

    monogramCount: dict[str, int]
    totalMonograms: int = 0

    distinctBigramCount: dict[str, int]
    totalDistinctBigrams: int = 0

    overlappedBigramCount: dict[str, int]
    totalOverlappedBigrams: int = 0

    whitespace: str | None
    isWhitespace: bool = False
    previousSymbol: str | None = None

    # Alphabet is a dictionary uppercase -> lowercase.
    # \x00 in uppercase means a character that is not included in the alphabet and
    # can be interpreted as \x00 lowercase. Sequences of \x00 counts as a single symbol.
    def __init__(self, alphabet: dict[str, str]):
        self.alphabet = set(alphabet.values())
        self.up2low = alphabet

        # Initialize dictionaries.
        self.monogramCount = {c: 0 for c in self.alphabet}
        self.overlappedBigramCount = {c1 + c2: 0 for c1 in self.alphabet for c2 in self.alphabet}
        self.whitespace = alphabet[NULL] if NULL in alphabet else None
        if not self.whitespace is None:
            # Remove double whitespace bigram.
            del self.overlappedBigramCount[self.whitespace*2]

        self.distinctBigramCount = self.overlappedBigramCount.copy()

    # Update monogram count with currentSymbol and previousSymbol for bigrams.
    def updateNgramCounts(self, currentSymbol: str) -> None:
        self.monogramCount[currentSymbol] += 1
        self.totalMonograms += 1
        
        # previousSymbol absent for the first letter
        if not self.previousSymbol is None:
            # Total overlapped bigrams count is one less than monograms count.
            self.overlappedBigramCount[self.previousSymbol + currentSymbol] += 1
            self.totalOverlappedBigrams += 1

            # Total distinct bigrams count is half of monograms count.
            if self.totalMonograms % 2 == 0:
                self.distinctBigramCount[self.previousSymbol + currentSymbol] += 1
                self.totalDistinctBigrams += 1

    def handleText(self, text: str) -> None:
        for c in text:
            c = c.lower()
            # All characters that are not included in the alphabet are considered whitespaces.
            if c not in self.alphabet or (not self.whitespace is None and c == self.whitespace):
                # If whitespace is not provided in alphabet -- skip it.
                if self.whitespace is None:
                    continue

                # There can be only one whitespace, so we skip 2 or more spaces in a row.
                if self.isWhitespace:
                    continue
                
                self.updateNgramCounts(self.whitespace)
                self.isWhitespace = True
                self.previousSymbol = self.whitespace
                continue

            self.isWhitespace = False
            self.updateNgramCounts(c)
            self.previousSymbol = c

    # Create a DataFrame for monogram frequencies.
    def formMonogramDF(self) -> pd.DataFrame:
        monoDF = pd.DataFrame()
        monoFreq = calculateFrequency(self.monogramCount, self.totalMonograms)

        monogramCol: list[str] = []
        freqCol: list[Decimal] = []

        # Split frequencies dictionary into two columns (monograms with corresponding frequencies by index).
        for monogram, freq in monoFreq.items():
            monogramCol.append(monogram)
            freqCol.append(freq)
        
        monoDF.insert(0, "Monogram", monogramCol, allow_duplicates=True)
        monoDF.insert(1, "Frequency", freqCol, allow_duplicates=True)
        return monoDF
    
    # Create a DataFrame for bigram frequencies.
    def formBigramDF(self, overlapped: bool = True) -> pd.DataFrame:
        biDF = pd.DataFrame()

        # Calculate frequencies depending on whether the bigrams can ovelap.
        biFreq: dict[str, Decimal] = {}
        if overlapped:
            biFreq = calculateFrequency(self.overlappedBigramCount, self.totalOverlappedBigrams)
        else:
            biFreq = calculateFrequency(self.distinctBigramCount, self.totalDistinctBigrams)

        bigramCol: list[str] = []
        bigramRow: list[str] = []

        # Split bigrams into headers: column (1st letter) and a row (2nd letter).
        for bigram in biFreq.keys():
            bigramRow.append(bigram[0])
            bigramCol.append(bigram[1])

        bigramCol.sort()
        bigramRow.sort()

        # Remove duplicates.
        bigramCol = removeDuplicates(bigramCol)
        bigramRow = removeDuplicates(bigramRow)

        # Pre-fill frequencies matrix with 0s.
        freqMatrix = fillEmpty(len(bigramCol), len(bigramRow))

        # Set the frequencies in corresponding cells. 
        for bigram, freq in biFreq.items():
            col = bigramRow.index(bigram[1])
            row = bigramCol.index(bigram[0])
            freqMatrix[col][row] = f"{(freq * Decimal(100)):.3f}"

        # Add row headers (column) to the sheet and the correspondig frequencies along with a column header.
        biDF.insert(0, "Bigram Letters (scale x100)", bigramRow, allow_duplicates=True)
        for i in range(len(bigramRow)):
            biDF.insert(i + 1, bigramCol[i], freqMatrix[i], allow_duplicates=True)

        return biDF

    # Create an Excel file with aggregated statistics.
    def statisticsToExcel(self, filename: str) -> None:
        # MONOGRAMS : Form columns monogram -> frequency.
        monoDF = self.formMonogramDF()

        # OVERLAPPED BIGRAMS : Form matrix for overlapped bigrams -> frequencies.
        oBiDF = self.formBigramDF(overlapped=True)

        # DISTINCT BIGRAMS : Form matrix for distinct bigrams -> frequencies.
        dBiDF = self.formBigramDF(overlapped=False)

        # CONVERSION TO EXCEL.
        with pd.ExcelWriter(filename + EXCEL_EXTENSION) as writer:
            monoDF.to_excel(writer, sheet_name="Monogram Statictic", index=False)
            oBiDF.to_excel(writer, sheet_name="Overlapped Bigram Statistic", index=False)
            dBiDF.to_excel(writer, sheet_name="Distinct Bigram Statistic", index=False)

        # CONVERION TO CSV.
        monoDF.to_csv(filename + CSV_EXTENSION, index=False)
        oBiDF.to_csv(filename + CSV_EXTENSION, index=False)
        dBiDF.to_csv(filename + CSV_EXTENSION, index=False)


# Fill NxM matrix (2D list) with 0s.
def fillEmpty(columns: int, rows: int) -> list[list[str]]:
    matrix: list[list[str]] = []
    for i in range(columns):
        matrix.append([])
        for _ in range(rows):
            matrix[i].append("0")
    return matrix


# Remove duplicates in a list.
def removeDuplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))


# Calculate frequency of each Ngram in text by dividing its occurences on total Ngram quantity.
def calculateFrequency(ngramCount: dict[str, int], totalNgrams: int) -> dict[str, Decimal]:
    # Since log(0) is undefined, add one to the amount of each ngrams.
    freqs = {ngram: Decimal(count) / Decimal(totalNgrams) for ngram, count in ngramCount.items()}
    return dict(sorted(freqs.items(), key=lambda item: item[1], reverse=True))


def calculateEntropy(frequencies: dict[str, Decimal]) -> Decimal:
    entropy = Decimal(0)
    for freq in frequencies.values():
        if not freq.is_zero():
            entropy -= freq * Decimal(log2(freq))
    return entropy / Decimal(len(list(frequencies.keys())[0]))


def sourceRedundancy(entropy: Decimal, symbolsCount: int) -> Decimal:
    return Decimal(1) - (entropy / Decimal(log2(symbolsCount)))


# Read text from file by blocks and process by handler.
# Handler should be an object method.
def readTextWithHandler(fileName: str, handler: Callable[[str], None]):
    with open(fileName, "r", encoding="utf-8") as f:
        textBlock = f.read(TEXT_BLOCK_SIZE)
        handler(textBlock)


def main():
    # CLI
    argparser = argparse.ArgumentParser(prog="Entropy calculator", 
                                    description="This script calculates the specific entropy for monograms and bigrams of the given text.",
                                    usage="main.py pathToFile")
    argparser.add_argument('path', nargs='?', help='path to text file')
    args = argparser.parse_args()
    if not args.path:
        argparser.print_help()
        exit(0)
    if not os.path.isfile(args.path):
        argparser.print_help()
        exit(0)
    fileName: str = args.path

    generalCalc = EntropyCalculator(STANDARD_ALPHABET)
    whitespacedCalc = EntropyCalculator(STANDARD_ALPHABET_WHITESPACE)

    readTextWithHandler(fileName, generalCalc.handleText)
    readTextWithHandler(fileName, whitespacedCalc.handleText)

    freqs = calculateFrequency(generalCalc.monogramCount, generalCalc.totalMonograms)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monograms (without spaces):", entropy)
    print("Source redundancy on monograms (without spaces):", sourceRedundancy(entropy, len(generalCalc.alphabet)))
    print("Monogram (without spaces) frequencies:")
    pprint.pp(freqs)

    print()

    freqs = calculateFrequency(generalCalc.overlappedBigramCount, generalCalc.totalOverlappedBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on bigrams (overlapped) (without spaces):", entropy)
    print("Source redundancy on bigrams (overlapped) (without spaces):", sourceRedundancy(entropy, len(generalCalc.alphabet)))

    print()

    freqs = calculateFrequency(generalCalc.distinctBigramCount, generalCalc.totalDistinctBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on bigrams (not overlapped/distinct) (without spaces):", entropy)
    print("Source redundancy on bigrams (not overlapped/distinct) (without spaces):", sourceRedundancy(entropy, len(generalCalc.alphabet)))

    print()

    freqs = calculateFrequency(whitespacedCalc.monogramCount, whitespacedCalc.totalMonograms)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monogram characters (with spaces):", entropy)
    print("Source redundancy on monogram characters (with spaces):", sourceRedundancy(entropy, len(whitespacedCalc.alphabet)))
    print("Monogram (with spaces) frequencies:")
    pprint.pp(freqs)

    print()

    freqs = calculateFrequency(whitespacedCalc.overlappedBigramCount, whitespacedCalc.totalOverlappedBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monogram characters (overlapped) (with spaces):", entropy)
    print("Source redundancy on monogram characters (overlapped) (with spaces):", sourceRedundancy(entropy, len(whitespacedCalc.alphabet)))

    print()

    freqs = calculateFrequency(whitespacedCalc.distinctBigramCount, whitespacedCalc.totalDistinctBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monogram characters (not overlapped) (with spaces):", entropy)
    print("Source redundancy on monogram characters (not overlapped) (with spaces):", sourceRedundancy(entropy, len(whitespacedCalc.alphabet)))

    generalCalc.statisticsToExcel(STATICTIC_OUTPUT_FILE)
    whitespacedCalc.statisticsToExcel(STATICTIC_OUTPUT_FILE_WHITESPACED)


if __name__ == "__main__":
    main()
