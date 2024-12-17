import matplotlib.pyplot as plt
from collections import Counter

# Російський алфавіт
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def read_cipher_text(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read().replace('ё', 'е').replace('\n', '').upper()

def calculate_index_of_coincidence(text):
    n = len(text)
    frequency = Counter(text)
    index_of_coincidence = sum(f * (f - 1) for f in frequency.values()) / (n * (n - 1))
    return index_of_coincidence

def split_text_into_blocks(cipher_text, r):
    blocks = ['' for _ in range(r)]
    for i, char in enumerate(cipher_text):
        blocks[i % r] += char
    return blocks

def average_index_of_coincidence(cipher_text, max_key_length):
    indices = []
    for r in range(2, max_key_length + 1):
        blocks = split_text_into_blocks(cipher_text, r)
        block_indices = [calculate_index_of_coincidence(block) for block in blocks]
        avg_ic = sum(block_indices) / len(block_indices)
        indices.append((r, avg_ic))
    return indices

def plot_indices(indices):
    lengths, values = zip(*indices)
    plt.plot(lengths, values, marker='o')
    plt.title('Індекс відповідності для різних довжин ключа')
    plt.xlabel('Довжина ключа')
    plt.ylabel('Індекс відповідності')
    plt.grid(True)
    plt.show()

# Прочитати зашифрований текст
cipher_text = read_cipher_text('task3.txt')

# Максимальна довжина ключа для перевірки
max_key_length = 30  # Можна вибрати більше значення за потреби

# Обчислити індекси відповідності
indices = average_index_of_coincidence(cipher_text, max_key_length)

# Побудувати діаграму
plot_indices(indices)
