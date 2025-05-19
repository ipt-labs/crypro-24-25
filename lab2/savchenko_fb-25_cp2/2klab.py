import random

def generate_key(length):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    return ''.join(random.choice(alphabet) for _ in range(length))

def vigenere_encrypt(text, key):
  
    encrypted_text = []
    key_length = len(key)
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    m = len(alphabet)
    
    for i, char in enumerate(text):
        if char in alphabet:
            x_i = alphabet.index(char)
            k_i = alphabet.index(key[i % key_length])
            y_i = (x_i + k_i) % m
            encrypted_text.append(alphabet[y_i])
        else:
            encrypted_text.append(char) 
    
    return ''.join(encrypted_text)


lengths = [2, 3, 4, 5] + list(range(10, 21))
keys = {length: generate_key(length) for length in lengths}


with open("f.txt", "r", encoding="utf-8") as file:
    text = file.read()


encrypted_texts = {length: vigenere_encrypt(text, key) for length, key in keys.items()}


for length, encrypted_text in encrypted_texts.items():
    print(f"Ключ ({length} символів): {keys[length]}")
    print("Зашифрований текст:", encrypted_text)
    print()
