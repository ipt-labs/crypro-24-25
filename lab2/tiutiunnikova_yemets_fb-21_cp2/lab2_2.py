import re
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# ----ФІЛТРАЦІЯ --------
def filter_text(text):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    return ''.join(filter(lambda char: char in alphabet, text.lower())), alphabet

# ----РОЗРАХУНОК ІНДЕКСУ ВІДПОВІДНОСТІ----
def index_of_coincidence(text):
    n = len(text)
    freq = Counter(text)
    return sum(count * (count - 1) for count in freq.values()) / (n * (n - 1)) if n > 1 else 0

# ----ІНДЕКСИ ДЛЯ РІЗНОЇ ДОВЖИНИ КЛЮЧА----
def ic_for_keys(text, max_len=30):
    text, alphabet = filter_text(text)
    ics = {}
    
    for key_len in range(2, max_len + 1):
        blocks = ['' for _ in range(key_len)]
        for i, char in enumerate(text):
            blocks[i % key_len] += char
        
        block_ics = [index_of_coincidence(block) for block in blocks]
        ics[key_len] = sum(block_ics) / len(block_ics) if block_ics else 0
    
    return ics

# ----ОЦІНКА ЙМОВІРНОГО КЛЮЧА----
def estimate_key(text, key_len):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    text = filter_text(text)[0]
    
    blocks = ['' for _ in range(key_len)]
    for i, char in enumerate(text):
        blocks[i % key_len] += char
    
    freq_data = {char: [] for char in alphabet}
    common_chars = []
    keys = []
    
    likely_char = 'о'

    for block in blocks:
        freq = Counter(block)
        for char in alphabet:
            freq_data[char].append(freq.get(char, 0))
        
        most_common, _ = freq.most_common(1)[0]
        common_chars.append(most_common)
        
        y = alphabet.index(most_common)
        x = alphabet.index(likely_char)
        key = (y - x) % len(alphabet)
        
        keys.append(alphabet[key])
    
    return freq_data, common_chars, keys

with open("task3.txt", "r", encoding='utf-8') as file:
    text = file.read()

# ----АНАЛІЗ І.В.----
max_len = 30
ics = ic_for_keys(text, max_len)

for key_len, value in ics.items():
    print(f"Довжина ключа: {key_len}, Індекс відповідності: {value:.6f}")

best_len = max(ics, key=ics.get)
print(f"Довжина ключа з максимальним індексом відповідності: {best_len}")

# ----ГРАФІК----
plt.figure(figsize=(10, 5))
plt.scatter(ics.keys(), ics.values(), color='blue', marker='o')
plt.xlabel('Довжина ключа')
plt.ylabel('Індекс відповідності')
plt.xticks(range(2, max_len + 1))
plt.show()

# ----------------------------------------
freq_data, common_chars, keys = estimate_key(text, best_len)
df = pd.DataFrame(freq_data)
df.index.name = 'Літера'
df.to_excel("task3_table.xlsx", index=True)

print("Ймовірні значення ключа:", keys)
