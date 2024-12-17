import matplotlib.pyplot as plt
from collections import Counter

def index_of_coincidence(text):
    """
    Обчислює індекс відповідності за заданою формулою.
    """
    n = len(text) 
    if n <= 1:  # Якщо текст занадто короткий, IC = 0
        return 0

    # Частоти символів у тексті
    frequencies = Counter(text)

    # Розрахунок IC за формулою
    numerator = sum(f * (f - 1) for f in frequencies.values())
    denominator = n * (n - 1)
    ic = numerator / denominator

    return ic

keys = {
    2: 'на',
    3: 'это',
    4: 'едва',
    5: 'сорок',
    10: 'содержание',
    11: 'переговоров',
    12: 'избалованных',
    13: 'присоединении',
    14: 'приехаввберлин',
    15: 'новосильцевузнал',
    16: 'завладениегенуей',
    17: 'милойэнтузиасткой',
    18: 'увлечениеидеальными',
    19: 'общественнымположением',
    20: 'необманутьожиданийлюдей'
}
# Читаємо відкритий текст
with open('cleaned_lab2.1.txt', 'r', encoding='utf-8') as file:
    open_text = file.read()

# Розрахунок IC для відкритого тексту
ic_open_text = index_of_coincidence(open_text)

# Розрахунок IC для зашифрованих текстів
ic_encrypted_texts = {}
for length in keys.keys():
    encrypted_path = f'encrypted/encrypted_with_key_length_{length}.txt'
    with open(encrypted_path, 'r', encoding='utf-8') as file:
        encrypted_text = file.read()
        ic_encrypted_texts[length] = index_of_coincidence(encrypted_text)

print(f"Індекс відповідності для відкритого тексту: {ic_open_text:.5f}")
for length, ic in ic_encrypted_texts.items():
    print(f"Індекс відповідності для шифротексту (ключ довжини {length}): {ic:.5f}")

# Побудова гістограми
keys_lengths = ['Відкритий текст'] + [str(length) for length in ic_encrypted_texts.keys()]
ic_values = [ic_open_text] + list(ic_encrypted_texts.values())

plt.figure(figsize=(10, 6))
plt.bar(keys_lengths, ic_values, width=0.6)
plt.title("Індекси відповідності для відкритого тексту та шифротекстів")
plt.xlabel("Довжина ключа")
plt.ylabel("Індекс відповідності (IC)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()