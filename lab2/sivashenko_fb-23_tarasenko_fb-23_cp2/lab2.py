import re
from collections import Counter

def index_of_coincidence(text):
    n = len(text)
    if n == 0:
        return 0  

    letter_counts = Counter(text)
    ic = sum(count * (count - 1) for count in letter_counts.values()) / (n * (n - 1))
    return ic


def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
    letters = re.sub(r'[^а-яА-ЯёЁ]', '', text)  
    return letters.lower()


def vigenere_encrypt(text, key):
    encrypted_text = []
    key = key.lower()  
    key_length = len(key)
    key_index = 0

    for char in text:
        if 'а' <= char <= 'я':  
            shift = ord(key[key_index % key_length]) - ord('а')  
            encrypted_char = chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
            encrypted_text.append(encrypted_char)
            key_index += 1

    return ''.join(encrypted_text)


def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key = key.lower()  
    key_length = len(key)
    key_index = 0

    for char in ciphertext:
        if 'а' <= char <= 'я':  
            shift = ord(key[key_index % key_length]) - ord('а') 
            decrypted_char = chr((ord(char) - ord('а') - shift) % 32 + ord('а'))
            decrypted_text.append(decrypted_char)
            key_index += 1

    return ''.join(decrypted_text)


keys = ["ар", "дос", "метр", "текст", "деньгинесм", "йщомпывояьп", "агенствонедв", "гурманынеедят", "журеавыофчцкыю", "славаукраинегер"]

file_path = "lab2.txt" 

text = read_text(file_path)
print("Початковий текст:\n", text)

for key in keys:
    encrypted = vigenere_encrypt(text, key)
    print(f"\nЗашифрований текст (довжина ключа {len(key)}):\n", encrypted)

    decrypted = vigenere_decrypt(encrypted, key)
    print(f"\nРозшифрований текст (довжина ключа {len(key)}):\n", decrypted)
    print()  

# Шифруємо текст для кожного ключа та зберігаємо шифртексти
ciphertexts = {}
for key in keys:
    encrypted = vigenere_encrypt(text, key)
    ciphertexts[key] = encrypted

plaintext_ic = index_of_coincidence(text)
print(f"\nІндекс відповідності відкритого тексту: {plaintext_ic}")
print("\nШифртексти та їх індекси відповідності:")
for key, ciphertext in ciphertexts.items():
    ic = index_of_coincidence(ciphertext)
    print(f"Ключ: {len(key)} | {ic}")




