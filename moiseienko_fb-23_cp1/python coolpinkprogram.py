import entropy_assessment

def calculate_entropy(text, n):
    # Створюємо словник для збереження частот n-грам
    freq = {}
    text_length = len(text)
    
    for i in range(text_length - n + 1):
        n_gram = text[i:i+n]
        if n_gram in freq:
            freq[n_gram] += 1
        else:
            freq[n_gram] = 1
    
    # Обчислюємо ентропію
    entropy = 0.0
    for key in freq.keys():
        p = freq[key] / (text_length - n + 1)
        entropy -= p * math.log2(p)
    
    return entropy

def main():
    # Відкриваємо файл з текстом
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ').lower()
        text = text.replace('ё', 'е').replace('ъ', 'ь')
    
    # Підрахунок ентропії для n = 10, 20, 30 та виконання 50 експериментів
    for n in [10, 20, 30]:
        entropies = []
        for i in range(50):
            entropy = calculate_entropy(text, n)
            entropies.append(entropy)
        avg_entropy = sum(entropies) / len(entropies)
        print(f'Average entropy for n={n} over 50 experiments: {avg_entropy}')

if __name__ == "__main__":
    main()
