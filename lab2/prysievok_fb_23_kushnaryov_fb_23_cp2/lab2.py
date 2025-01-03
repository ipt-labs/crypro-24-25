import re
from collections import Counter
from math import log

def read_txt_file(path):
    with open(path, 'r', encoding='UTF-8') as file:
        text = file.read()
    return text

def clean_text_no_spaces(text):
    new_text = re.sub(r'[^а-яё]', '', text.lower())
    return new_text

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='UTF-8') as file:
        file.write(text)


def encrypt_text(text, key):
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    # alphabet = "abcdefghijklmnopqrstuvwxyz"
    key_nums = [alphabet.find(s) for s in key]
    dictionary = {}
    encrypted_text = ''
    for i in range(len(text)):
        if text[i] in alphabet:
            shift = key_nums[i%len(key)]
            char_id = alphabet.find(text[i])
            new_char = alphabet[(char_id + shift) % len(alphabet)]
            encrypted_text = encrypted_text + new_char
        else:
            encrypted_text = encrypted_text + text[i]
    
    return encrypted_text

def get_ic(text):
    n = len(text)
    char_counts = Counter(text)
    return sum(count * (count -1) for count in char_counts.values())/(n * (n - 1))

def do_lab2():
    text = read_txt_file('alice_clean.txt')
    keys = ['на','уже','годы','алиса']
    for i in range(10,21):
        keys.append('смежныхснеюпроблемкоторые'[:i])
    print(f"open text ic: {get_ic(text)}")
    for key in keys:
        file_name = f"alice_encrypted{len(key)}.txt"
        encrypted_text = encrypt_text(text,key)
        save_text_to_file(encrypted_text, file_name)
        print(f"saved to '{file_name}', ic: {get_ic(encrypted_text)}, key: '{key}'")


do_lab2()


# text = read_txt_file('alice.txt')
# text_clean = read_txt_file('alice_clean.txt')

# for key in {'на','уже','годы','алиса','','','','','',''}:
#     encrypt_text(text_clean, key)

# save_text_to_file(encrypted_text_clean, 'alice_encrypted.txt')
