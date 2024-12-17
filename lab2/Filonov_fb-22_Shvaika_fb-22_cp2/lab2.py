import re
from argparse import ArgumentParser
from collections import Counter


def formatting_text(text):
    with open(text, 'r') as file:
        text = file.read()

    text = text.lower().replace('ё', 'е')
    text = re.sub(r'[^а-яё ]', ' ', text)
    text = ''.join(text.split())

    return text


def encrypt(text, r, letter_index, index_leter): 
    encrypted_text = [] 
    ri = 0 
    for i in text: 
        letter = (letter_index[i] + letter_index[r[ri]]) % 32 
        letter = index_leter[letter] 
        encrypted_text.append(letter) 
        ri = (ri + 1) % len(r) 

    return ''.join(encrypted_text)


def count_indices(text): 
    count_letters = Counter(text) 
    sum = 0 
    for i in count_letters.values(): 
        sum += i * (i - 1) 
    sum = sum/(len(text)*(len(text)-1)) 
    return sum


def find_len_r(text): 
    dif=float('inf') 
    I = 0.0545 
    r = 0 
    for i in range(2, 31): 
        sum = 0 
        for j in range(2, i + 1): 
            sum += count_indices(text[j::i]) 
        if (I - sum / i) < dif: 
            dif = I - sum / i 
            r = i 
    return r 


def find_r(text, letter_index, index_letter): 
    len_r = find_len_r(text) 
    r = [] 
    for i in range(len_r): 
        Yi = text[i::len_r] 
        count_letters = Counter(Yi) 
        letter = count_letters.most_common(1)[0] 
        r.append(index_letter[(letter_index[letter[0]]-14) % 32]) 

    return ''.join(r) 


def decrypt(text, r, letter_index, index_leter): 
    encrypted_text = [] 
    ri=0 
    for i in text: 
        letter = (letter_index[i] - letter_index[r[ri]]) % 32 
        letter = index_leter[letter] 
        encrypted_text.append(letter) 
        ri = (ri + 1) % len(r) 
    return ''.join(encrypted_text) 


def main_func():
    arg_parser = ArgumentParser(
        prog='Програма для лабораторної роботи №2. Виконали студенти групи ФБ-22 Швайка та Філонов',
        description='''Програма створена для шифрування/розшифрування вхідного тексту
        та для підрахунку індексів відкритого тексту та шифротекстів'''
    )

    arg_parser.add_argument('text', help='Шлях до вхідного тексту для шифрування')
    arg_parser.add_argument('cleaned_text', help='Шлях до зберігання очищеного тексту')
    arg_parser.add_argument('encrypted_text', help='Шлях до зберігання зашифрованого тексту')
    arg_parser.add_argument('key', type=str, help='Ключ для шифрування')
    arg_parser.add_argument('-enc_file', help='Зашифрований файл для нашого варіанту')
    arg_parser.add_argument('-dec_file', help='Файл для збереження результату розшифрування')

    args = arg_parser.parse_args()

    alp = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

    # Очищаємо початковий текст від зайвих символів і записуємо у файл
    cleaned_text = formatting_text(args.text)
    with open(args.cleaned_text, 'w') as file_for_cleaned_text:
        file_for_cleaned_text.write(cleaned_text)

    letter_index = {letter: index for index, letter in enumerate(alp)}
    index_letter = {index: letter for index, letter in enumerate(alp)}

    # Зашифровуємо текст    
    encrypted_text = encrypt(cleaned_text, args.key, letter_index, index_letter)
    with open(args.encrypted_text, 'w') as file_for_encrypted_text:
        file_for_encrypted_text.write(encrypted_text)

    # Якщо переданий текст для розшифрування для завдання №3, 
    # то спочатку форматуємо його і потім розшифровуємо
    if args.enc_file:
        cleaned_dec_text = formatting_text(args.enc_file)
        r = find_r(cleaned_dec_text, letter_index, index_letter)        
        decrypted_text = decrypt(cleaned_dec_text, 'возвращениеджинна', letter_index, index_letter)
        print('Ключ для зашифрованого тексту', f'знайдений програмою: {r}', 'правильний ключ: возвращениеджинна', sep='\n\t')
        with open(args.dec_file, 'w') as dec_result:
            dec_result.write(decrypted_text)

    print(f'''Сума індексів відповідності:
          а)для початкового тексту: {count_indices(cleaned_text)}
          б)для зашифрованого тексту: {count_indices(encrypted_text)}
    ''')


main_func()
