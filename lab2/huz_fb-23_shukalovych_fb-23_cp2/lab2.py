import os
import re
from collections import Counter
import matplotlib.pyplot as plt
import csv

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

#шифр Віженера
def vigenere(plaintext, key):
    cipher_text = []
    key_length = len(key)
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    
    for i, char in enumerate(plaintext):
        if char.islower():
            key_char = key[i % key_length].lower()  
            shift = alphabet.index(key_char)  # Отримаємо зсув за ключем
            encrypted_char = alphabet[(alphabet.index(char) + shift) % 33]
            cipher_text.append(encrypted_char)
    return ''.join(cipher_text)

#зробили так, щоб текст був неперервним
def load_and_clean_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        text = text.lower()
        text = re.sub(r'[^а-яё]', '', text)
        return text
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено")
        return None

#функція для обрахунку індекса відповідності
def index_of_coincidence(text):
    letter_counts = Counter(text)
    n = sum(letter_counts.values())

    total_sum = sum(Nt * (Nt - 1) for Nt in letter_counts.values())
    index = total_sum / (n * (n - 1))

    return index

#функція для обрахунку індексів відповідності для усіх значень ключа шифр. та відкритого тексту
def calculate_indexes_for_keys(clear_text, *key_ranges):
    ic_dict = {}

    ic_value = index_of_coincidence(clear_text) #обрахунок індексу для ВТ
    ic_dict[0] = ic_value

    for key_range in key_ranges:
        for key_choice in key_range:
            try:
                with open(f"encrypted_text/encrypted_{key_choice}.txt", 'r', encoding='utf-8') as file:
                    content = file.read()
                    ic_value = index_of_coincidence(content)
                    ic_dict[key_choice] = ic_value
            except FileNotFoundError:
                #print(f"Файл 'encrypted_{key_choice}.txt' не знайдено.")
                ic_dict[key_choice] = None

    return ic_dict

# Знаходимо довжину ключа
def find_key_length(text, max_key_length=31):
    best_key_length = 0
    closest_ic_diff = float('inf')
    ic_dict = {}
    ic_russian = 0.0557

    for key_length in range(2, max_key_length + 1):
        avg_ic = 0

        # Розбиваємо текст на блоки
        for i in range(key_length):
            block = text[i::key_length]
            avg_ic += index_of_coincidence(block)

        avg_ic /= key_length
        ic_diff = abs(avg_ic - ic_russian)
        ic_dict[key_length] = avg_ic

        if ic_diff < closest_ic_diff:
            closest_ic_diff = ic_diff
            best_key_length = key_length

    return best_key_length, ic_dict

# Частотний аналіз для пошуку ключа
def find_key(text, key_length):
    key = []
    most_common_letter = "о"
    var_alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

    for i in range(key_length):
        block = text[i::key_length]
        most_common = Counter(block).most_common(1)[0][0]
        key_letter = (var_alphabet.index(most_common) - var_alphabet.index(most_common_letter)) % len(var_alphabet)
        key.append(var_alphabet[key_letter])

    return ''.join(key)

#функція для розшифрування тексту за варіантом
def vigenere_decrypt(cipher_text, key):
    decrypted_text = []
    key_length = len(key)
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    
    for i, char in enumerate(cipher_text):
        if char in alphabet:  
            key_char = key[i % key_length].lower()
            shift = alphabet.index(key_char) 
            decrypted_char = alphabet[(alphabet.index(char) - shift) % 32]  
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)  
    
    return ''.join(decrypted_text)

#побудова гістаграми
def plot_histogram(data):
    filtered_data = {k: v for k, v in data.items() if v is not None}

    if not filtered_data:
        print("Немає значень для побудови гістограми.")
        return
    #print(filtered_data)
    keys = list(filtered_data.keys())
    values = list(filtered_data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(keys)), values, color='pink')

    plt.title('Гістограма індексів відповідності')
    plt.xlabel('r')
    plt.ylabel('I')

    plt.xticks(range(len(keys)), keys)

    plt.tight_layout()
    plt.show()


def main(ic_results, clear_text, clear_text2, key_length, ic_dict):
    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Вивести текст")
        print("2. Зашифрувати текст")
        print("3. Обчислити індекси відповідності")
        print("4. Розшифрувати текст")
        print("5. Діаграми")
        print("6. Вийти")
        
        user_choice = input("Виберіть опцію: ").strip()
        
        if user_choice == '6':
            print(BLUE + " /}___/}❀\n( • . •)\n/ >    > Byeee" + RESET)
            break
        
        if user_choice == '1':
            while True:
                print(YELLOW + "\n-♥-Меню виведення тексту-♥-" + RESET)
                print("0. Повернутись")
                print("1. Вивести текст")
                print("2. Вивести текст за варіантом")
                    
                text_choice = input("\nВиберіть опцію: ").strip()
                
                if text_choice == '1':
                    print(f"\nОригінальний текст:\n{clear_text}")
                
                elif text_choice == '2':
                    print(f"\nОригінальний текст::\n{clear_text2}")
                
                elif text_choice == '0':
                    break  
                else:
                    print("Неправильний вибір. Спробуйте знову.")
        
        elif user_choice == '2':
            print(YELLOW + "\n-♥-Введіть довжину ключа для шифрування-♥-" + RESET + '\nМожливі довжини ключа: 2-5, 10-20')
            
            while True:
                key_choice = input("\nВведіть довжину ключа або '0' для повернення: ").strip()
                if key_choice == '0':
                    break
                
                # Ключі для шифрування
                encryption_keys = {'2': 'хи', '3': 'мяу', '4': 'сова', '5': 'осень',  
                                   '10': 'абитуриент', '11': 'бессмертный', '12': 'концентратор',
                                   '13': 'глазированный', '14': 'мультипликатив', '15': 'ухлёстывавшийся',
                                   '16': 'христадельфианин', '17': 'яфетидологический', 
                                   '18': 'задокументировавши', '19': 'жизнеобеспечивающий',  
                                   '20': 'евростандартизировав'}

                key = encryption_keys.get(key_choice)
                
                if not key:
                    print(f"Неправильний вибір '{key_choice}'. Спробуйте знову.")
                    continue  

                cipher_text = vigenere(clear_text, key)
                print(f"\nЗашифрований текст:\n{cipher_text}")

                directory = "encrypted_text"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                output_file = os.path.join(directory, f"encrypted_{key_choice}.txt") #збереження зашифрованого тексту
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(cipher_text)

                print(f"\nЗашифрований текст збережено у '{output_file}'")
                
        elif user_choice == '3':
            print(
                YELLOW + "\n-♥-Введіть довжину ключа для знаходження індексу відповідності-♥-" + RESET + '\nМожливі довжини ключа: 2-5, 10-20')

            print(f'\nІндекс відповідності для відкритого тексту: {ic_results[0]}')

            while True:
                key_choice = int(input("\nВведіть довжину ключа або '0' для повернення: "))
                if key_choice == 0:
                    break

                if key_choice in ic_results and ic_results[key_choice] is not None:
                    print(f'\nІндекс відповідності для ключа {key_choice}: {ic_results[key_choice]}')
                else:
                    try:
                        with open(f"encrypted_text/encrypted_{key_choice}.txt", 'r', encoding='utf-8') as file:
                            content = file.read()
                            ic_value = index_of_coincidence(content)
                            ic_results[key_choice] = ic_value
                            print(f'\nІндекс відповідності для ключа {key_choice}: {ic_value}')
                    except FileNotFoundError:
                        print(f"Файл 'encrypted_{key_choice}.txt' не знайдено. Зашифруйте спочатку текст з відповідним ключем.")

        elif user_choice == '4':
            key = find_key(clear_text2, key_length)
            key_v = "громыковедьма" #підібрали "вручну" після отриманого результату

            print(f"Довжина ключа: {key_length}")
            print(f"Підібраний ключ: {key}")
            print(f"Kлюч: {key_v}")

            decrypted_text = vigenere_decrypt(clear_text2, key_v)
            with open("decrypted_text.txt", "w", encoding="utf-8") as file:
                file.write(decrypted_text)
            print(f"\nРозшифрований текст:\n{decrypted_text}")
            print("\nРозшифрований текст збережено у decrypted_text.txt")

        elif user_choice == '5':
            while True:
                print(YELLOW + "\n-♥-Меню виведення діаграм-♥-" + RESET)
                print("0. Повернутись")
                print("1. Діаграма п.2")
                print("2. Діаграма п.3")

                dia_choice = input("\nВиберіть опцію: ").strip()

                if dia_choice == '1':
                    with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file, delimiter=';')

                        writer.writerow(['Key length', 'Compliance index'])

                        for key, value in ic_results.items():
                            writer.writerow([key, value])

                    print("Дані успішно записані у файл data.csv:)")
                    plot_histogram(ic_results)
                    #print(ic_results)
                elif dia_choice == '2':
                    plot_histogram(ic_dict)
                elif dia_choice == '0':
                    break
                else:
                    print("Неправильний вибір. Спробуйте знову.")
        else:
                print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":

    clear_text = load_and_clean_text("lab2.1.txt")
    clear_text2 = load_and_clean_text("lab2.2.txt")

    key_length, ic_dict = find_key_length(clear_text2)

    ic_results = calculate_indexes_for_keys(clear_text, range(2, 6), range(10, 21))

    main(ic_results, clear_text, clear_text2, key_length, ic_dict)

