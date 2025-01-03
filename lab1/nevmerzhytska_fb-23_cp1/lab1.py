import math
from collections import Counter

russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def redundancy(H, N):
    return 1 - (H / math.log2(N))


def analyze_text(text):
    text = ''.join([ch.lower() for ch in text if ch in russian_alphabet])

   
    letter_count = Counter(text)
    total_letters = sum(letter_count.values())
    letter_probabilities = [count / total_letters for count in letter_count.values()]
    
    
    H1 = entropy(letter_probabilities)
    N_letters = len(letter_count)  
    redundancy_letters = redundancy(H1, N_letters)
    
    
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    bigram_count = Counter(bigrams)
    total_bigrams = sum(bigram_count.values())
    bigram_probabilities = [count / total_bigrams for count in bigram_count.values()]
    
    
    H2 = entropy(bigram_probabilities)
    N_bigrams = len(letter_count) ** 2  
    redundancy_bigrams = redundancy(H2, N_bigrams)
    
    
    bigrams_no_overlap = [text[i:i+2] for i in range(0, len(text) - 1, 2)]
    bigram_count_no_overlap = Counter(bigrams_no_overlap)
    total_bigrams_no_overlap = sum(bigram_count_no_overlap.values())
    bigram_probabilities_no_overlap = [count / total_bigrams_no_overlap for count in bigram_count_no_overlap.values()]
    
    
    H2_no_overlap = entropy(bigram_probabilities_no_overlap)
    redundancy_bigrams_no_overlap = redundancy(H2_no_overlap, N_bigrams)
    
    return (letter_count, bigram_count, bigram_count_no_overlap, H1, H2, H2_no_overlap, 
            redundancy_letters, redundancy_bigrams, redundancy_bigrams_no_overlap)


def analyze_text_without_spaces(text):
    text_without_spaces = ''.join([ch.lower() for ch in text if ch in russian_alphabet])
    return analyze_text(text_without_spaces)


def read_text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


text = read_text_from_file('text1.txt')  


letter_count, bigram_count, bigram_count_no_overlap, H1, H2, H2_no_overlap, redundancy_letters, redundancy_bigrams, redundancy_bigrams_no_overlap = analyze_text(text)


print("\nЧастота букв у тексті:")
print("{:<10} {:<10} {:<10}".format("Символ", "Кількість", "Частота"))
letter_table = [(letter, count, count / sum(letter_count.values())) for letter, count in letter_count.items()]

letter_table.sort(key=lambda x: x[1], reverse=True)
for letter, count, frequency in letter_table:
    print("{:<10} {:<10} {:<10.5f}".format(letter, count, frequency))


print("\nЧастота біграм в тексті з перетинами:")
print("{:<10} {:<10} {:<10}".format("Символ", "Кількість", "Частота"))
bigram_table = [(bigram, count, count / sum(bigram_count.values())) for bigram, count in bigram_count.items()]

bigram_table.sort(key=lambda x: x[1], reverse=True)
for bigram, count, frequency in bigram_table:
    print("{:<10} {:<10} {:<10.5f}".format(bigram, count, frequency))


print("\nЧастота біграм в тексті без перетинів:")
print("{:<10} {:<10} {:<10}".format("Символ", "Кількість", "Частота"))
bigram_no_overlap_table = [(bigram, count, count / sum(bigram_count_no_overlap.values())) for bigram, count in bigram_count_no_overlap.items()]

bigram_no_overlap_table.sort(key=lambda x: x[1], reverse=True)
for bigram, count, frequency in bigram_no_overlap_table:
    print("{:<10} {:<10} {:<10.5f}".format(bigram, count, frequency))


print("\nЕнтропія для символів з пробілами:", H1)
print("Ентропія для символів без пробілів:", analyze_text_without_spaces(text)[3])
print("Ентропія для біграм з пробілами і перетинами:", H2)
print("Ентропія для біграм з пробілами без перетинів:", H2_no_overlap)
print("Ентропія для біграм без пробілів з перетинами:", analyze_text_without_spaces(text)[4])
print("Ентропія для біграм без пробілів без перетинів:", analyze_text_without_spaces(text)[5])

print("\nНадлишковість для символів з пробілами:", redundancy_letters)
print("Надлишковість для символів без пробілів:", redundancy(analyze_text_without_spaces(text)[3], len(set(text.replace(' ', '').lower()))))
print("Надлишковість для біграм з пробілами і перетинами:", redundancy_bigrams)
print("Надлишковість для біграм з пробілами без перетинів:", redundancy_bigrams_no_overlap)
print("Надлишковість для біграм без пробілів з перетинами:", redundancy(analyze_text_without_spaces(text)[4], len(set(text.replace(' ', '').lower()))**2))
print("Надлишковість для біграм без пробілів без перетинів:", redundancy(analyze_text_without_spaces(text)[5], len(set(text.replace(' ', '').lower()))**2))
