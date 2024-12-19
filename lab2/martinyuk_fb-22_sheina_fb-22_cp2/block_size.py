import re
from collections import Counter

def calculate_ic(input_text):
    total_chars = len(input_text)
    if total_chars == 0:
        return 0  

    char_frequencies = Counter(input_text)
    ic_value = sum(freq * (freq - 1) for freq in char_frequencies.values()) / (total_chars * (total_chars - 1))
    return ic_value


def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    cleaned_content = re.sub(r'[^а-яА-ЯёЁ]', '', content)  
    return cleaned_content.lower()


def enc_vig(plain_text, cipher_key):
    result = []
    cipher_key = cipher_key.lower()  
    key_size = len(cipher_key)
    key_pos = 0

    for symbol in plain_text:
        if 'а' <= symbol <= 'я':  
            offset = ord(cipher_key[key_pos % key_size]) - ord('а')  
            encrypted_symbol = chr((ord(symbol) - ord('а') + offset) % 32 + ord('а'))
            result.append(encrypted_symbol)
            key_pos += 1

    return ''.join(result)


def dec_vig(encrypted_text, cipher_key):
    result = []
    cipher_key = cipher_key.lower()  
    key_size = len(cipher_key)
    key_pos = 0

    for symbol in encrypted_text:
        if 'а' <= symbol <= 'я':  
            offset = ord(cipher_key[key_pos % key_size]) - ord('а')  
            decrypted_symbol = chr((ord(symbol) - ord('а') - offset) % 32 + ord('а'))
            result.append(decrypted_symbol)
            key_pos += 1

    return ''.join(result)


keys_list = ["да", "кто", "литр", "слово", "далсьпщнаб", "чиназесчина", "саунтресчина", "детиголодаютт", "зачемяэтоделаю", "помогитеявзалож"]

file_path = "lab2.txt" 

original_text = load_text(file_path)
print("Исходный текст:\n", original_text)

for cipher_key in keys_list:
    encrypted_text = enc_vig(original_text, cipher_key)
    print(f"\nЗашифрованный текст (длина ключа {len(cipher_key)}):\n", encrypted_text)

    decrypted_text = dec_vig(encrypted_text, cipher_key)
    print(f"\nРасшифрованный текст (длина ключа {len(cipher_key)}):\n", decrypted_text)
    print()  

# Шифрование текста для каждого ключа и вычисление индексов
encrypted_texts = {}
for cipher_key in keys_list:
    encrypted_texts[cipher_key] = enc_vig(original_text, cipher_key)

original_ic = calculate_ic(original_text)
print(f"\nИндекс совпадений исходного текста: {original_ic}")
print("\nЗашифрованные тексты и их индексы совпадений:")
for cipher_key, cipher_text in encrypted_texts.items():
    ic = calculate_ic(cipher_text)
    print(f"Ключ: {len(cipher_key)} | {ic}")
