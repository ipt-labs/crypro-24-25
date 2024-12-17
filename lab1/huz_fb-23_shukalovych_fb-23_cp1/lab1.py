import re
from collections import Counter
import math
import csv

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

#очищений текст з пробілами
def clean_text():
    with open('lab1.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.lower()
    cleaned = re.sub(r'[^а-яё\s]+', '', content)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    return cleaned

#очищений текст без пробілів
def remove_spaces(text):
    return text.replace(" ", "")

#кількість літер без пробілів
def count_letters_without_spaces(text):
    letter_counts = Counter(re.findall(r'[а-яё]', text))
    return letter_counts

#кількість літер з пробілами
def count_letters_with_spaces(text):
    letter_counts_with_spaces = Counter(text)
    return letter_counts_with_spaces

#загальна кількість літер
def total_letter_count(letter_counts):
    return sum(letter_counts.values())

#частота літер
def letter_frequencies(letter_counts, total_count):
    frequencies = {}
    for letter, count in letter_counts.items():
        frequencies[letter] = count / total_count
    sorted_frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    return sorted_frequencies

#кількість біграм з перетином
def count_bigrams(text):
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    bigram_counts = Counter(bigrams)
    return bigram_counts

#кількість біграм без перетину
def count_bigrams_no_overlap(text):
    bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]
    bigram_counts = Counter(bigrams)
    return bigram_counts

#загальна кількість біграм
def count_total_bigrams(bigram_counts):
    total_bigrams = sum(bigram_counts.values())
    return total_bigrams

#частота біграм
def bigram_frequencies(bigram_counts, total_bigrams):
    frequencies = {}
    for bigram, count in bigram_counts.items():
        frequencies[bigram] = count / total_bigrams
    return frequencies

#виведення кількості біграм
def print_bigram_table(bigram_counts):
    formatted_bigrams = []
    for bigram, count in bigram_counts.items():
        formatted_bigrams.append(f'"{bigram}" - {count}')
    print("\nКількість біграм:")
    for i in range(0, len(formatted_bigrams), 8):
        print("  ".join(formatted_bigrams[i:i + 8]))

#виведення частот біграм у вигляді матриці (34x34)
def print_bigram_frequencies(bigram_frequencies):
    letters = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
    n = len(letters)

    matrix = [[0.0] * n for _ in range(n)]

    for bigram, frequency in bigram_frequencies.items():
        if bigram[0] in letters and bigram[1] in letters:
            i = letters.index(bigram[0])
            j = letters.index(bigram[1])
            matrix[i][j] = frequency

    header = "    " + "   ".join(f"{letter:^5}" for letter in letters)
    print(header)

    print("    " + "-----" * 54)

    for i, row in enumerate(matrix):
        row_str = f"{letters[i]} | " + " ".join(f"{frequency:.5f}" for frequency in row)
        print(row_str)
        print("    " + "-----" * 54)


#обчислення ентропії для літер
def entropy_H1(letter_frequencies):
    entropy_value = 0
    for p_i in letter_frequencies.values():
        if p_i > 0:
            entropy_value -= p_i * math.log2(p_i)

    return entropy_value

#обчислення ентропії для біграм
def entropy_H2(bigram_frequencies):
    entropy = 0
    for frequency in bigram_frequencies.values():
        if frequency > 0:
            entropy -= frequency * math.log2(frequency)
    return entropy / 2


# функція для збереження кількості та частоти літер у CSV
def save_letter_counts_and_frequencies_to_csv(filename, letter_counts, letter_frequencies):
    letter_data = [(letter, letter_counts[letter], letter_frequencies.get(letter, 0)) for letter in letter_counts]

    sorted_letter_data = sorted(letter_data, key=lambda x: x[2], reverse=True)

    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Літера', 'Кількість', 'Частота'])

        for letter, count, frequency in sorted_letter_data:
            writer.writerow([letter, count, f"{frequency:.6f}"])


# Запис кількості та частоти біграм у файл CSV
def save_bigram_counts_and_frequencies_to_csv(filename, bigram_counts, bigram_frequencies):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Біграма', 'Кількість', 'Частота'])

        for bigram in sorted(bigram_counts.keys(), key=lambda item: bigram_counts[item], reverse=True):
            count = bigram_counts[bigram]
            frequency = bigram_frequencies.get(bigram, 0)
            writer.writerow([bigram, count, f"{frequency:.6f}"])

def text_menu(cleaned):
    while True:
        print(YELLOW + "\n-♥- Обробка тексту -♥-" + RESET)
        print("1. Вивести текст з пробілами")
        print("2. Вивести текст без пробілів")
        print("3. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            print("\nТекст з пробілами:")
            print(cleaned)
        elif choice == '2':
            print("\nТекст без пробілів:")
            print(remove_spaces(cleaned))
        elif choice == '3':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")

def letters_menu(letter_counts_without_spaces, total_count_without_spaces, letter_counts_with_spaces, total_count_with_spaces):
    while True:
        print(YELLOW + "\n-♥- Аналіз літер -♥-" + RESET)
        print("1. Вивести кількість літер без пробілів")
        print("2. Вивести частоту літер без пробілів")
        print("3. Вивести кількість літер з пробілами")
        print("4. Вивести частоту літер з пробілами")
        print("5. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            print("\nКількість літер:")
            for letter, count in letter_counts_without_spaces.items():
                print(f"{letter}: {count}")
            print(f"Загальна кількість літер: {total_count_without_spaces}")
        elif choice == '2':
            frequencies = letter_frequencies(letter_counts_without_spaces, total_count_without_spaces)
            print("\nЧастота літер:")
            for letter, frequency in frequencies.items():
                print(f"Частота літери '{letter}': {frequency}")
        elif choice == '3':
            print("\nКількість літер:")
            for letter, count in letter_counts_with_spaces.items():
                print(f"{letter}: {count}")
            print(f"Загальна кількість символів: {total_count_with_spaces}")
        elif choice == '4':
            frequencies_with_spaces = letter_frequencies(letter_counts_with_spaces, total_count_with_spaces)
            print("\nЧастота літер:")
            for letter, frequency in frequencies_with_spaces.items():
                print(f"Частота символу '{letter}': {frequency}")
        elif choice == '5':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")

def bigram_menu(bigram_counts_without_spaces, bigram_counts_with_spaces, count_bigrams_no_overlap_with_spaces, count_bigrams_no_overlap_no_spaces):
    while True:
        print(YELLOW + "\n-♥- Аналіз біграм -♥-" + RESET)
        print(BLUE + 15*"-" + "З пробілами" + 15*"-" + RESET)
        print("1. Вивести кількість біграм з перетином")
        print("2. Вивести кількість біграм без перетину")
        print("3. Вивести частоту біграм з перетином")
        print("4. Вивести частоту біграм без перетину")
        print(BLUE + 15*"-" + "Без пробілів" + 15*"-" + RESET)
        print("5. Вивести кількість біграм з перетином")
        print("6. Вивести кількість біграм без перетину")
        print("7. Вивести частоту біграм з перетином")
        print("8. Вивести частоту біграм без перетину")
        print("9. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            print_bigram_table(bigram_counts_with_spaces)
            print(f"Загальна кількість біграм: {count_total_bigrams(bigram_counts_with_spaces)}")
        elif choice == '2':
            print_bigram_table(count_bigrams_no_overlap_with_spaces)
            print(f"Загальна кількість біграм: {count_total_bigrams(count_bigrams_no_overlap_with_spaces)}")
        elif choice == '3':
            total_bigrams = sum(bigram_counts_with_spaces.values())
            bigram_frequencies_table = bigram_frequencies(bigram_counts_with_spaces, total_bigrams)
            print_bigram_frequencies(bigram_frequencies_table)
        elif choice == '4':
            total_bigrams = sum(count_bigrams_no_overlap_with_spaces.values())
            bigram_frequencies_table = bigram_frequencies(count_bigrams_no_overlap_with_spaces, total_bigrams)
            print_bigram_frequencies(bigram_frequencies_table)
        elif choice == '5':
            print_bigram_table(bigram_counts_without_spaces)
            print(f"Загальна кількість біграм: {count_total_bigrams(bigram_counts_without_spaces)}")
        elif choice == '6':
            print_bigram_table(count_bigrams_no_overlap_no_spaces)
            print(f"Загальна кількість біграм: {count_total_bigrams(count_bigrams_no_overlap_no_spaces)}")
        elif choice == '7':
            total_bigrams = sum(bigram_counts_without_spaces.values())
            bigram_frequencies_table = bigram_frequencies(bigram_counts_without_spaces, total_bigrams)
            print_bigram_frequencies(bigram_frequencies_table)
        elif choice == '8':
            total_bigrams = sum(count_bigrams_no_overlap_no_spaces.values())
            bigram_frequencies_table = bigram_frequencies(count_bigrams_no_overlap_no_spaces, total_bigrams)
            print_bigram_frequencies(bigram_frequencies_table)
        elif choice == '9':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")

def entropy_menu(letter_frequencies_without_spaces, letter_frequencies_with_spaces, bigram_frequencies_without_spaces, bigram_frequencies_with_spaces, bigram_frequencies_no_overlap_no_spaces,
                         bigram_frequencies_no_overlap_with_spaces):
    while True:
        print(YELLOW + "\n-♥- Ентропія -♥-" + RESET)
        print("1. H1 з пробілами")
        print("2. H1 без пробілів")
        print("3. H2 з пробілами, з перетинами")
        print("4. H2 без пробілів, з перетинами")
        print("5. H2 з проблілами, без перетинів")
        print("6. H2 без проблілами, без перетинів")
        print("7. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            h1_1 = entropy_H1(letter_frequencies_with_spaces)
            print(f"\nЕнтропія H1: {h1_1:.5f}")
        elif choice == '2':
            h1_2 = entropy_H1(letter_frequencies_without_spaces)
            print(f"\nЕнтропія H1: {h1_2:.5f}")
        elif choice == '3':
            h2_3 = entropy_H2(bigram_frequencies_with_spaces)
            print(f"\nЕнтропія H2: {h2_3:.5f}")
        elif choice == '4':
            h2_4 = entropy_H2(bigram_frequencies_without_spaces)
            print(f"\nЕнтропія H2: {h2_4:.5f}")
        elif choice == '5':
            h2_5 = entropy_H2(bigram_frequencies_no_overlap_with_spaces)
            print(f"\nЕнтропія H2: {h2_5:.5f}")
        elif choice == '6':
            h2_6 = entropy_H2(bigram_frequencies_no_overlap_no_spaces)
            print(f"\nЕнтропія H2: {h2_6:.5f}")
        elif choice == '7':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")

def main():
    cleaned = clean_text()
    cleaned_without_spaces = remove_spaces(cleaned)

    #обчислення даних без врахування пробілу
    letter_counts_without_spaces = count_letters_without_spaces(cleaned)
    total_count_without_spaces = total_letter_count(letter_counts_without_spaces)
    letter_frequencies_without_spaces = letter_frequencies(letter_counts_without_spaces, total_count_without_spaces)

    bigram_counts_without_spaces = count_bigrams(cleaned_without_spaces)
    count_bigrams_no_overlap_no_spaces = count_bigrams_no_overlap(cleaned_without_spaces)
    bigram_frequencies_without_spaces = bigram_frequencies(bigram_counts_without_spaces, count_total_bigrams(bigram_counts_without_spaces))
    bigram_frequencies_no_overlap_no_spaces = bigram_frequencies(count_bigrams_no_overlap_no_spaces, count_total_bigrams(count_bigrams_no_overlap_no_spaces))

    #обчислення даних з врахуванням пробілу
    letter_counts_with_spaces = count_letters_with_spaces(cleaned)
    total_count_with_spaces = total_letter_count(letter_counts_with_spaces)
    letter_frequencies_with_spaces = letter_frequencies(letter_counts_with_spaces, total_count_with_spaces)

    bigram_counts_with_spaces = count_bigrams(cleaned)
    count_bigrams_no_overlap_with_spaces = count_bigrams_no_overlap(cleaned)
    bigram_frequencies_with_spaces = bigram_frequencies(bigram_counts_with_spaces, count_total_bigrams(bigram_counts_with_spaces))
    bigram_frequencies_no_overlap_with_spaces = bigram_frequencies(count_bigrams_no_overlap_with_spaces, count_total_bigrams(count_bigrams_no_overlap_with_spaces))

    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Обробка тексту")
        print("2. Аналіз літер")
        print("3. Аналіз біграм")
        print("4. Ентропія")
        print("5. Запис усіх даних у файли")
        print("6. Вийти")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            text_menu(cleaned)
        elif choice == '2':
            letters_menu(letter_counts_without_spaces, total_count_without_spaces, letter_counts_with_spaces, total_count_with_spaces)
        elif choice == '3':
            bigram_menu(bigram_counts_without_spaces,bigram_counts_with_spaces, count_bigrams_no_overlap_with_spaces, count_bigrams_no_overlap_no_spaces)
        elif choice == '4':
            entropy_menu(letter_frequencies_without_spaces,
                         letter_frequencies_with_spaces,
                         bigram_frequencies_without_spaces,
                         bigram_frequencies_with_spaces,
                         bigram_frequencies_no_overlap_no_spaces,
                         bigram_frequencies_no_overlap_with_spaces)
        elif choice == '5':
            save_letter_counts_and_frequencies_to_csv('data/letter_counts_and_frequencies_without_spaces.csv',
                                                      letter_counts_without_spaces, letter_frequencies_without_spaces)
            save_letter_counts_and_frequencies_to_csv('data/letter_counts_and_frequencies_with_spaces.csv',
                                                      letter_counts_with_spaces, letter_frequencies_with_spaces)
            save_bigram_counts_and_frequencies_to_csv('data/bigram_counts_without_spaces.csv', bigram_counts_without_spaces,
                                                      bigram_frequencies_without_spaces)
            save_bigram_counts_and_frequencies_to_csv('data/bigram_counts_no_overlap_without_spaces.csv',
                                                      count_bigrams_no_overlap_no_spaces,
                                                      bigram_frequencies_no_overlap_no_spaces)
            save_bigram_counts_and_frequencies_to_csv('data/bigram_counts_with_spaces.csv', bigram_counts_with_spaces,
                                                      bigram_frequencies_with_spaces)
            save_bigram_counts_and_frequencies_to_csv('data/bigram_counts_no_overlap_with_spaces.csv',
                                                      count_bigrams_no_overlap_with_spaces,
                                                      bigram_frequencies_no_overlap_with_spaces)

            print("Дані успішно записані у файли CSV.")
        elif choice == '6':
            print(BLUE + " /}___/}❀\n( • . •)\n/ >    > Byeee" + RESET)
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз")

if __name__ == "__main__":
    main()
