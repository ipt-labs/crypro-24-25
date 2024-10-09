import re
from collections import defaultdict
import math
import csv

def save_to_csv(result, filename):
    with open(filename, mode='w', newline='', encoding='windows-1251') as file:
        writer = csv.writer(file, delimiter=';')  
        writer.writerow(["Character", "Frequency"])  
        for char, freq in result.items():
            writer.writerow([char, freq])  
    print(f"[+] Результат збережено у файл {filename}")

def calculate_entropy_monograms(freq_dict):
    total_count = sum(freq_dict.values())
    entropy = 0.0
    
    for freq in freq_dict.values():
        if freq > 0:
            p = freq / total_count
            entropy -= p * math.log2(p)
    
    return entropy

def calculate_entropy_bigrams(bigram_freq_dict):
    total_count = sum(bigram_freq_dict.values())
    entropy = 0.0
    
    for freq in bigram_freq_dict.values():
        if freq > 0:
            p = freq / total_count
            entropy -= (p * math.log2(p)) / 2
    
    return entropy


def calculate_redundancy(H, alphabet_size):
    H0 = math.log2(alphabet_size)
    redundancy = 1 - (H / H0) if H0 > 0 else 0
    
    return redundancy


def change_bad(char):
    if char == 'ё':
        return 'е'
    elif char == 'ъ':
        return 'ь'
    else:
        return char

def calc_freq(dicti, counter):
    for key,value in dicti.items():
        value = value/counter
        dicti[key] = value
    return dicti

#Частота однограм із пробілом
def count_russian_letters(filename, counter):
    freq_dict = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    for char in text:
        char = char.lower()
        if re.match(r'[а-яА-ЯёЁ ]', char):
            char = change_bad(char)
            freq_dict[char] += 1
    freq_dict = calc_freq(freq_dict, counter)
    return freq_dict

#Частота однограм без пробілу
def count_russian_letters_without(filename, counter_w):
    freq_dict = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    for char in text:
        char = char.lower()
        if re.match(r'[а-яА-ЯёЁ]', char):
            char = change_bad(char)
            freq_dict[char] += 1
    freq_dict = calc_freq(freq_dict, counter_w)
    return freq_dict

#Частота біграм без пробілів з кроком 2
def count_russian_letter_pairs_skip_spaces(filename, counter_w):
    freq_dict = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    i = 0
    while i < len(text) - 1:
        
        first_char = change_bad(text[i].lower())
        second_char = change_bad(text[i + 1].lower())
        if first_char == ' ':
            i += 1
            continue
        
        j = i + 1
        while j < len(text) and text[j] == ' ':
            j += 1
        if j >= len(text):
            break

        second_char = change_bad(text[j].lower())
        pair = first_char + second_char
        if re.match(r'[а-яА-ЯёЁ]{2}', pair):
            freq_dict[pair] += 1
        i = j + 1
    freq_dict = calc_freq(freq_dict, counter_w)
    return freq_dict

#Частота біграм з пробілами з кроком 2
def count_russian_letter_pairs_with_step(filename, counter):
    freq_dict = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    for i in range(0, len(text) - 1, 2):
        first_char = change_bad(text[i].lower())
        second_char = change_bad(text[i + 1].lower())
        pair = first_char + second_char
        if re.match(r'[а-яА-ЯёЁ ]{2}', pair):
            freq_dict[pair] += 1
    freq_dict = calc_freq(freq_dict, counter)
    return freq_dict

#Частота біграм з пробілами з кроком 1
def count_russian_letter_pairs(filename, counter):
    freq_dict = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    for i in range(len(text) - 1):
        first_char = change_bad(text[i].lower())
        second_char = change_bad(text[i + 1].lower())
        pair = first_char + second_char
        if re.match(r'[а-яё ]{2}', pair):
            freq_dict[pair] += 1
    freq_dict = calc_freq(freq_dict, counter)
    return freq_dict

#Частота біграм без пробілів з кроком 1
def count_russian_letter_pairs1_skip_spaces(filename, counter_w):
    freq_dict = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    i = 0
    while i < len(text) - 1:
        first_char = change_bad(text[i].lower())

        if first_char == ' ':
            i += 1
            continue
        j = i + 1
        while j < len(text) and text[j] == ' ':
            j += 1
        if j >= len(text):
            break
        second_char = change_bad(text[j].lower())
        pair = first_char + second_char
        if re.match(r'[а-яё]{2}', pair):
            freq_dict[pair] += 1
        i += 1
    freq_dict = calc_freq(freq_dict, counter_w)
    return freq_dict

#Підрахунок символів у тексті з пробілом
def count_letters(filename):
    counter = 0
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    for char in text:
        if re.match(r'[а-яА-ЯёЁ ]', char):
            counter += 1
    return counter

#Підрахунок символів у тексті без пробілу
def count_letters_without(filename):
    counter = 0
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    for char in text:
        if re.match(r'[а-яА-ЯёЁ]', char):
            counter += 1
    return counter

# Виклик функції
filename = 'text.txt'  
counter = count_letters(filename)
counter_w = count_letters_without(filename)
alphabet_size = 34
alphabet_size_w = 33

#Монограми
#З пробілом
mono = count_russian_letters(filename, counter)

#Без пробілу
mono_w = count_russian_letters_without(filename, counter_w)

#Біграми (крок 1)
#З пробілом
bigram = count_russian_letter_pairs(filename, counter)

#Без пробілу
bigram_w = count_russian_letter_pairs1_skip_spaces(filename, counter_w)

#Біграми (крок 2)
#З пробілом
bigram_2 = count_russian_letter_pairs_with_step(filename, counter)

#Без пробілу
bigram_w2 = count_russian_letter_pairs_skip_spaces(filename, counter_w)

print("\n============= Збереження результатів =============")
save_to_csv(mono, 'monograms.csv')
save_to_csv(mono_w, 'monograms_w.csv')
save_to_csv(bigram, 'bigrams.csv')
save_to_csv(bigram_w, 'bigrams_w.csv')
save_to_csv(bigram_2, 'bigrams_2.csv')
save_to_csv(bigram_w2, 'bigrams_w2.csv')

print("\n============= Обрахування ентропії =============")

h1 = calculate_entropy_monograms(mono)
print(f"Ентропія H1: {h1}")

h1_w = calculate_entropy_monograms(mono_w)
print(f"Ентропія H1 без пробілу: {h1_w}")

h2 = calculate_entropy_bigrams(bigram)
print(f"Ентропія H2 з кроком 1 : {h2}")

h2_w = calculate_entropy_bigrams(bigram_w)
print(f"Ентропія H2 з кроком 1 без пробілу : {h2_w}")

h2_2 = calculate_entropy_bigrams(bigram_2)
print(f"Ентропія H2 з кроком 2 : {h2_2}")

h2_w2 = calculate_entropy_bigrams(bigram_w2)
print(f"Ентропія H2 з кроком 2 без пробілу : {h2_w2}")

print("\n============= Обрахування надлишковості джерела відкритого тексту =============")

redundancy_h1 = calculate_redundancy(h1, alphabet_size)
print(f"Redundancy h1: {redundancy_h1}")

redundancy_h1_w = calculate_redundancy(h1_w, alphabet_size_w)
print(f"Redundancy h1_w: {redundancy_h1_w}")

redundancy_h2 = calculate_redundancy(h2, alphabet_size)
print(f"Redundancy h2: {redundancy_h2}")

redundancy_h2_w = calculate_redundancy(h2_w, alphabet_size_w)
print(f"Redundancy h2_w: {redundancy_h2_w}")

redundancy_h2_2 = calculate_redundancy(h2_2, alphabet_size)
print(f"Redundancy h2_2: {redundancy_h2_2}")

redundancy_h2_w2 = calculate_redundancy(h2_w2, alphabet_size_w)
print(f"Redundancy h2_w2: {redundancy_h2_w2}")
