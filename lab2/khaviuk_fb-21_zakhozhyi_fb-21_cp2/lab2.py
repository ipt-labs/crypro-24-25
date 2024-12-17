import matplotlib.pyplot as plt
from collections import Counter
from tabulate import tabulate

FILENAME_FOR_ENCRYPTION = "./toEncrypt.txt"
FILENAME_FOR_DECRYPTION = "./toDecrypt.txt"
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def prepare_text(text):
    text = text.lower().replace('ё', 'е')
    return ''.join([char for char in text if char in ALPHABET])

def vigenere_encrypt(plaintext, key):
    ciphertext = []
    for i, char in enumerate(plaintext):
        p = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        c = (p+k) % len(ALPHABET)
        ciphertext.append(ALPHABET[c])
    return ''.join(ciphertext)

def calculate_frequencies(text):
    freqs = Counter(text)
    total = sum(freqs.values())
    return {char: freq / total for char, freq in freqs.items()}

def index_of_coincidence(text):
    freqs = Counter(text)
    n = sum(freqs.values())
    if n <= 1:
        return 0
    ic_sum = sum(f*(f-1) for f in freqs.values())
    return ic_sum/(n*(n-1))

def colision(text, r):
    return sum(1 for i in range(len(text) - r) if text[i] == text[i + r])

def plot_dr_sequence(collision):
    plt.figure(figsize=(12, 6))
    plt.plot(collision.keys(), collision.values(), color='blue', marker='o', label="Dr Sequence")
    plt.xlabel('Довжина ключа (r)')
    plt.ylabel('Кількість збігів Dr')
    plt.title('Послідовність Dr для різних значень r')
    plt.legend()
    plt.grid()
    plt.show()

def find_key_length(ciphertext, max_key_length=30):
    avg_ics = {}
    colisions = {}
    for key_length in range(1, max_key_length + 1):
        ics = [index_of_coincidence(ciphertext[i::key_length]) for i in range(key_length)]
        avg_ics[key_length] = sum(ics) / len(ics)
        colisions[key_length] = colision(ciphertext, key_length)
    likely_key_length = max(avg_ics, key=avg_ics.get)
    return likely_key_length, avg_ics, colisions

def plot_index_of_coincidence(avg_ics):
    plt.figure(figsize=(12, 6))
    plt.bar(avg_ics.keys(), avg_ics.values(), color='yellow', label="Index of Coincidence")
    plt.xlabel('Довжина ключа')
    plt.ylabel('Індекс відповідності')
    plt.title('Аналіз довжини ключа')
    plt.legend()
    plt.grid()
    plt.show()

def display_ic_table(avg_ics):
    table = [[r, ic] for r, ic in avg_ics.items()]
    print("Таблиця значень індексів відповідності для різних значень r:")
    print(tabulate(table, headers=["r (Довжина ключа)", "Індекс відповідності"], tablefmt="grid"))

def frequency_analysis(text):
    return sorted(calculate_frequencies(text).items(), key=lambda item: item[1], reverse=True)

def decrypt_vigenere(ciphertext, key):
    plaintext = []
    for i, char in enumerate(ciphertext):
        c = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        p = (c - k) % len(ALPHABET)
        plaintext.append(ALPHABET[p])
    return ''.join(plaintext)

def find_vigenere_key(ciphertext, key_length):
    key = []
    for i in range(key_length):
        nth_subtext = ciphertext[i::key_length]
        freq_analysis = frequency_analysis(nth_subtext)
        most_common_letter = freq_analysis[0][0]
        likely_key_letter_index = (
            ALPHABET.index(most_common_letter) - ALPHABET.index('о')) % len(ALPHABET)
        
        likely_key_letter = ALPHABET[likely_key_letter_index]
        key.append(likely_key_letter)
    
    return ''.join(key)

def main():
    with open(FILENAME_FOR_ENCRYPTION, 'r', encoding='utf-8') as f:
        plaintext = prepare_text(f.read())
    
    # Шифрування тексту кожним із ключів та виведення результату
    keys = ["ты", "кот", "зима", "весна", "киноактриса", "абстрагирование"]
    encrypted_texts = [(key, vigenere_encrypt(plaintext, key)) for key in keys]
    
    print("Індекси відповідності для текстів:")
    print(f"Відкритий текст: {index_of_coincidence(plaintext)}")
    for key, ciphertext in encrypted_texts:
        ic = index_of_coincidence(ciphertext)
        print(f"\nКлюч: {key} | Індекс відповідності: {ic}")
        print(f"Зашифрований текст (перші 200 символів): {ciphertext[:200]}")
    
    with open(FILENAME_FOR_DECRYPTION, 'r', encoding='utf-8') as f:
        ciphertext = prepare_text(f.read())
    
    likely_key_length, avg_ics, colisions = find_key_length(ciphertext)
    print(f"\nЙмовірна довжина ключа: {likely_key_length}")
    
    display_ic_table(avg_ics) # відображення таблиці індексів відповідності
    plot_index_of_coincidence(avg_ics) # побудува графіку індексів відповідності
    plot_dr_sequence(colisions) # побудува графіку для послідовності Dr
    probable_key = find_vigenere_key(ciphertext, likely_key_length)
    print(f"\nВідновлений потенційно правильний ключ: {probable_key}")

    nearly_decrypted_text = decrypt_vigenere(ciphertext, probable_key)
    print(f"\nМайже розшифрований текст: {nearly_decrypted_text[:200]}...")

    print("-" * 100)
    guessed_key = "возвращениеджинна"
    print(f"\nВідновлений правильний ключ: {guessed_key}")
    decrypted_text = decrypt_vigenere(ciphertext, guessed_key)
    print(f"\nПовністю розшифрований текст: {decrypted_text[:200]}...")

if __name__ == "__main__":
    main()