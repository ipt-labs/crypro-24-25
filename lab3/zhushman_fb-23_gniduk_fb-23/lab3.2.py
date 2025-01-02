from collections import Counter

def read_text_from_file(file_path):
    """
    Зчитує текст із файлу та видаляє пробіли.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return ''.join(filter(str.isalnum, text.lower()))

def calculate_bigram_frequencies(text):
    """
    Обчислює частоти біграм у тексті.
    """
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]  # Створюємо всі біграми
    total_bigrams = len(bigrams)  # Загальна кількість біграм
    bigram_counts = Counter(bigrams)  # Підраховуємо кількість кожної біграми
    bigram_frequencies = {bigram: count / total_bigrams for bigram, count in bigram_counts.items()}  # Частота
    return bigram_frequencies

def find_top_bigrams(file_path, top_n=5):
    """
    Знаходить топ N біграм із тексту у файлі.
    """
    text = read_text_from_file(file_path)
    frequencies = calculate_bigram_frequencies(text)
    top_bigrams = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:top_n]  # Топ N біграм за частотою
    return top_bigrams

file_path = '05.txt' 
top_bigrams = find_top_bigrams(file_path)

print(f"Топ-5 біграм із файлу {file_path}:")
for bigram, frequency in top_bigrams:
    print(f"{bigram}: {frequency:.4f}")
