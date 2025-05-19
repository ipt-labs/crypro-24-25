import numpy as np
from collections import Counter


RUSSIAN_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

def calculate_ic(text, alphabet):
    frequencies = [text.count(char) for char in alphabet]
    n = len(text)
    numerator = sum(f * (f - 1) for f in frequencies)
    denominator = n * (n - 1)
    return numerator / denominator if denominator > 0 else 0

def split_text_by_key_length(text, key_length):
    return [''.join(text[i::key_length]) for i in range(key_length)]

def find_key_length(ciphertext, max_key_length=20, alphabet=RUSSIAN_ALPHABET):
    ics = []
    for key_length in range(1, max_key_length + 1):
        groups = split_text_by_key_length(ciphertext, key_length)
        avg_ic = np.mean([calculate_ic(group, alphabet) for group in groups])
        ics.append(avg_ic)
    return ics

def find_key(ciphertext, key_length, alphabet):
    key = []
    groups = split_text_by_key_length(ciphertext, key_length)
    for group in groups:
        group_counter = Counter(group)
        most_common = group_counter.most_common(1)[0][0]
        shift = (alphabet.index(most_common) - alphabet.index('о')) % len(alphabet)
        key.append(alphabet[shift])
    return ''.join(key)

def vigenere_decrypt(ciphertext, key, alphabet):
    key_length = len(key)
    key_indices = [alphabet.index(k) for k in key]
    decrypted_text = []
    
    for i, char in enumerate(ciphertext):
        if char in alphabet:
            char_index = alphabet.index(char)
            decrypted_char = alphabet[(char_index - key_indices[i % key_length]) % len(alphabet)]
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)


def main():
    input_file = 'ciphertext.txt'

    with open(input_file, 'r', encoding='utf-8') as f:
        ciphertext = f.read().strip()

    filtered_ciphertext = ''.join([char for char in ciphertext if char in RUSSIAN_ALPHABET])

    ics = find_key_length(filtered_ciphertext)
    estimated_key_length = np.argmax(ics) + 1

    key_1 = find_key(filtered_ciphertext, estimated_key_length, RUSSIAN_ALPHABET)
    print(f'знайдений ключ:  {key_1}')
    key = 'улановсеребряныепули'
    print(f'правильний ключ: {key}')
    print()
    plaintext = vigenere_decrypt(filtered_ciphertext, key, RUSSIAN_ALPHABET)
    print(plaintext[:150])

    output_file = 'find_key.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Key found:  {key_1}\n")
        f.write(f"The right key: {key}\n")
        f.write("Decrypted text:\n")
        f.write(plaintext)
    
    print(f"The key and decrypted text are contained in the file {output_file}")

if __name__ == "__main__":
    main()
