import matplotlib.pyplot as plt
import pandas as pd  #використовую для роботи з DataFrame і збереження в Excel
from collections import Counter

file_crypto = "./2.txt"
alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def preprocess_text(text):
    #Підготовка тексту: зниження регістру, заміна 'ё' на 'е', видалення символів поза алфавітом.
    text = text.lower().replace('ё', 'е')
    return ''.join([char for char in text if char in alph])

def coincidence_index(text):
    #Обчислення індексу відповідності.
    char_counts = Counter(text)
    total_count = sum(char_counts.values())
    if total_count <= 1:
        return 0
    return sum(f * (f - 1) for f in char_counts.values()) / (total_count * (total_count - 1))

def calculate_frequency_distribution(text):
    #Обчислення частот символів у тексті.
    char_counts = Counter(text)
    total_chars = sum(char_counts.values())
    return {char: freq / total_chars for char, freq in char_counts.items()}

def detect_key_length(ciphertext, max_key_length=30):
    #Визначення ймовірної довжини ключа за допомогою індексів відповідності.
    ic_values = {}
    for key_length in range(1, max_key_length + 1):
        indices = [coincidence_index(ciphertext[i::key_length]) for i in range(key_length)]
        ic_values[key_length] = sum(indices) / len(indices)
    likely_length = max(ic_values, key=ic_values.get)
    return likely_length, ic_values

def visualize_ic_table(ic_values):
    #Побудова графіка індексів відповідності.
    plt.figure(figsize=(10, 5))
    plt.plot(list(ic_values.keys()), list(ic_values.values()), marker='o', color='green')
    plt.title("Індекс відповідності для різних довжин ключа")
    plt.xlabel("Довжина ключа")
    plt.ylabel("Індекс відповідності")
    plt.grid()
    plt.show()

def decrypt_vigenere(ciphertext, key):
    #Розшифровую текст за допомогою шифру Віженера.
    plaintext = []
    for i, char in enumerate(ciphertext):
        char_index = alph.index(char)
        key_index = alph.index(key[i % len(key)])
        decrypted_index = (char_index - key_index) % len(alph)
        plaintext.append(alph[decrypted_index])
    return ''.join(plaintext)

def recover_key(ciphertext, key_length):
    #Відновлення ключа на основі частотного аналізу.
    key = []
    for i in range(key_length):
        subtext = ciphertext[i::key_length]
        frequency = calculate_frequency_distribution(subtext)
        most_common_char = max(frequency, key=frequency.get)
        key_char_index = (alph.index(most_common_char) - alph.index('о')) % len(alph)
        key.append(alph[key_char_index])
    return ''.join(key)

def main():
    with open(file_crypto, 'r', encoding='utf-8') as file:
        ciphertext = preprocess_text(file.read())

    likely_length, ic_values = detect_key_length(ciphertext)
    print(f"Ймовірна довжина ключа: {likely_length}")

    visualize_ic_table(ic_values)

    # Зберігаємо індекси відповідності у файл Excel
    ic_df = pd.DataFrame(list(ic_values.items()), columns=["Довжина ключа", "Індекс відповідності"])
    ic_df.to_excel("ic_values.xlsx", index=False)
    print("Індекси відповідності збережено в файл 'ic_values.xlsx'.")

    potential_key = recover_key(ciphertext, likely_length)
    print(f"Відновлений ключ: {potential_key}")

    decrypted_sample = decrypt_vigenere(ciphertext, potential_key)
    print(f"Розшифрований текст (фрагмент): {decrypted_sample[:200]}...")

    actual_key = "возвращениеджинна"
    print(f"Справжній ключ: {actual_key}")
    fully_decrypted_text = decrypt_vigenere(ciphertext, actual_key)

    with open("decrypted.txt", "w", encoding="utf-8") as output_file:
        output_file.write(fully_decrypted_text)
    print("Розшифрований текст збережено у 'decrypted.txt'.")

if __name__ == "__main__":
    main()
