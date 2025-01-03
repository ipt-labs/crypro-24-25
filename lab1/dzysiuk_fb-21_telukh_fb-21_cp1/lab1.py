import re
from collections import Counter
import math

#Підготовка тексту
def text_preprocess(text, space_remove=False):
    text = text.lower()
    text = text.replace('ъ', 'ь').replace('ё', 'е')
    text = re.sub(r'[^а-я ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if space_remove:
        text = text.replace(' ', '')
    return text

#Підрахунок частот елементів
def calc_freq(elements):
    total = len(elements)
    freq = Counter(elements)
    return {elem: (count / total, count) for elem, count in freq.items()}

#Підрахунок ентропії
def calc_entropy(freq):
    return -sum(prob * math.log2(prob) for prob, _ in freq.values() if prob > 0)

#Підрахунок надлишковості
def calc_redundancy(entropy, alphabet_size):
    return 1 - (entropy / math.log2(alphabet_size))

#Запис результатів у файл
def write_results(filename, results):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(results)

if __name__ == "__main__":
    with open("text.txt", "r", encoding="utf-8") as file:
        text = file.read()

    text_spaces = text_preprocess(text)
    text_no_spaces = text_preprocess(text, space_remove=True)

    freq_with_spaces = calc_freq(text_spaces)
    h1_with_spaces = calc_entropy(freq_with_spaces)
    rd_with_spaces = calc_redundancy(h1_with_spaces, 32)

    freq_no_spaces = calc_freq(text_no_spaces)
    h1_no_spaces = calc_entropy(freq_no_spaces)
    rd_no_spaces = calc_redundancy(h1_no_spaces, 32)

    #Частоти біграм
    def get_bigrams(text, step=1):
        return [text[i:i+2] for i in range(0, len(text) - 1, step)]

    bigrams_spaces_overlap = calc_freq(get_bigrams(text_spaces, step=1))
    h2_spaces_overlap = calc_entropy(bigrams_spaces_overlap) / 2
    rd_bigrams_spaces_overlap = calc_redundancy(h2_spaces_overlap, 32)

    bigrams_spaces_no_overlap = calc_freq(get_bigrams(text_spaces, step=2))
    h2_spaces_no_overlap = calc_entropy(bigrams_spaces_no_overlap) / 2
    rd_bigrams_spaces_no_overlap = calc_redundancy(h2_spaces_no_overlap, 32)

    bigrams_no_spaces_overlap = calc_freq(get_bigrams(text_no_spaces, step=1))
    h2_no_spaces_overlap = calc_entropy(bigrams_no_spaces_overlap) / 2
    rd_bigrams_no_spaces_overlap = calc_redundancy(h2_no_spaces_overlap, 32)

    bigrams_no_spaces_no_overlap = calc_freq(get_bigrams(text_no_spaces, step=2))
    h2_no_spaces_no_overlap = calc_entropy(bigrams_no_spaces_no_overlap) / 2
    rd_bigrams_no_spaces_no_overlap = calc_redundancy(h2_no_spaces_no_overlap, 32)


    #Формування результатів і запис у різні файли
    l_results = []
    l_results.append("Частоти літер з пробілами:")
    for char, (prob, count) in sorted(freq_with_spaces.items(), key=lambda x: x[1][0], reverse=True):
        l_results.append(f"'{char}': {prob:.6f} ({count})")
    l_results.append(f"Ентропія H1: {h1_with_spaces:.6f}")
    l_results.append(f"Надлишковість: {rd_with_spaces:.6f}\n")

    l_results.append("Частоти літер без пробілів:")
    for char, (prob, count) in sorted(freq_no_spaces.items(), key=lambda x: x[1][0], reverse=True):
        l_results.append(f"'{char}': {prob:.6f} ({count})")
    l_results.append(f"Ентропія H1: {h1_no_spaces:.6f}")
    l_results.append(f"Надлишковість: {rd_no_spaces:.6f}\n")

    write_results("letters_results.txt", "\n".join(l_results))


    b_results = []

    b_results.append("Частоти біграм з пробілами (перетинаються):")
    for bigram, (prob, count) in sorted(bigrams_spaces_overlap.items(), key=lambda x: x[1][0], reverse=True):
        b_results.append(f"'{bigram}': {prob:.6f} ({count})")
    b_results.append(f"Ентропія H2: {h2_spaces_overlap:.6f}")
    b_results.append(f"Надлишковість: {rd_bigrams_spaces_overlap:.6f}\n")

    b_results.append("Частоти біграм з пробілами (не перетинаються):")
    for bigram, (prob, count) in sorted(bigrams_spaces_no_overlap.items(), key=lambda x: x[1][0], reverse=True):
        b_results.append(f"'{bigram}': {prob:.6f} ({count})")
    b_results.append(f"Ентропія H2: {h2_spaces_no_overlap:.6f}")
    b_results.append(f"Надлишковість: {rd_bigrams_spaces_no_overlap:.6f}\n")

    b_results.append("Частоти біграм без пробілів (перетинаються):")
    for bigram, (prob, count) in sorted(bigrams_no_spaces_overlap.items(), key=lambda x: x[1][0], reverse=True):
        b_results.append(f"'{bigram}': {prob:.6f} ({count})")
    b_results.append(f"Ентропія H2: {h2_no_spaces_overlap:.6f}")
    b_results.append(f"Надлишковість: {rd_bigrams_no_spaces_overlap:.6f}\n")

    b_results.append("Частоти біграм без пробілів (не перетинаються):")
    for bigram, (prob, count) in sorted(bigrams_no_spaces_no_overlap.items(), key=lambda x: x[1][0], reverse=True):
        b_results.append(f"'{bigram}': {prob:.6f} ({count})")
    b_results.append(f"Ентропія H2: {h2_no_spaces_no_overlap:.6f}")
    b_results.append(f"Надлишковість: {rd_bigrams_no_spaces_no_overlap:.6f}\n")

    write_results("bigrams_results.txt", "\n".join(b_results))

    print("Результати збережені у файли letters_results.txt і bigrams_results.txt")
