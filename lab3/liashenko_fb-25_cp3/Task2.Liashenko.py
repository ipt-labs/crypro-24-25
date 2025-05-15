from collections import Counter

def calculate_frequencies(text, n=2):
    text = text.lower()
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    frequencies = Counter(ngrams)
    return frequencies

def find_most_frequent_bigrams(frequencies, top_n=5):
    return sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:top_n]

def save_bigrams_to_file(bigrams, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for bigram, freq in bigrams:
            file.write(f"{bigram}: {freq}\n")

def analyze_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace(' ', '').lower()  

    bigram_frequencies = calculate_frequencies(text)
    top_bigrams = find_most_frequent_bigrams(bigram_frequencies)
    save_bigrams_to_file(top_bigrams, 'bigrams.txt')
    return top_bigrams

file_path = '08.txt'  
top_bigrams = analyze_text(file_path)

print("5 bigrams:")
for bigram, freq in top_bigrams:
    print(f"{bigram}: {freq}")


