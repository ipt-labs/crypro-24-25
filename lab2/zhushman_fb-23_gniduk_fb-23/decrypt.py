from collections import Counter

# Алфавіт
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
mod = len(alphabet)

def decrypt_with_key(text, key):
    """
    Розшифрування тексту за шифром Віженера із заданим ключем.
    """
    decrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        if char in alphabet:
            text_index = alphabet.index(char)
            key_index = alphabet.index(key[i % key_length])
            decrypted_char = alphabet[(text_index - key_index) % mod]
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

# Вхідні дані
with open('lab2.3.txt', 'r', encoding='utf-8') as file:
    cipher_text = file.read().replace('ё', 'е').strip()  # Видалення зайвих символів

# Уточнений ключ
refined_key = "делолисоборотней"

# Розшифрування тексту
decrypted_text = decrypt_with_key(cipher_text, refined_key)

# Збереження результату у файл
output_path = 'decrypted_lab2.3.txt'
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(decrypted_text)

print(f"Розшифрування завершено. Текст збережено у файл: {output_path}")
