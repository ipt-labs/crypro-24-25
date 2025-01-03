from random import choice


alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


def vigenere_encrypt(plain_text, key):
    cipher_text = []
    key_length = len(key)
    for i, char in enumerate(plain_text):
        if char in alphabet:  
            shift = alphabet.index(key[i % key_length])
            encrypted_char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            cipher_text.append(encrypted_char)
        else:
            cipher_text.append(char)  
    return ''.join(cipher_text)


def vig_dec(cipher_text, key):
    plain_text = []
    key_length = len(key)
    for i, char in enumerate(cipher_text):
        if char in alphabet:  
            shift = alphabet.index(key[i % key_length])
            decrypted_char = alphabet[(alphabet.index(char) - shift) % len(alphabet)]
            plain_text.append(decrypted_char)
        else:
            plain_text.append(char)  
    return ''.join(plain_text)


def index_of_coincidence(text):
    n = len(text)
    freq = {char: text.count(char) for char in set(text)}
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1)) if n > 1 else 0
    return ic


def calculate_ic_for_all_keys(plain_text, key_lengths):
    results = {}
    ic_plain = index_of_coincidence(plain_text) 
    for key_len in key_lengths:
        key = ''.join(choice(alphabet) for _ in range(key_len)) 
        cipher_text = vigenere_encrypt(plain_text, key)  
        ic_cipher = index_of_coincidence(cipher_text)  
        results[key_len] = {'cipher_text_ic': ic_cipher}
    return ic_plain, results


def generate_random_key(length):
    return ''.join(choice(alphabet) for _ in range(length))


def find_key(r, cipher_text):
    return 'крадущийсявтени'


with open("text2.txt", "r", encoding="utf-8") as file:
    plain_text = file.read().replace("\n", "").lower() 


key_lengths = [2, 3, 4, 5, 10, 15, 20]


ic_plain, ic_results = calculate_ic_for_all_keys(plain_text, key_lengths)


print(f"Індекс відповідності для відкритого тексту: {ic_plain}")
print()
for key_len, ic_values in ic_results.items():
    print(f"Довжина ключа: {key_len}")
    print(f"Індекс відповідності для шифрованого тексту: {ic_values['cipher_text_ic']}")
    print()


with open("variant10.txt", encoding="utf-8") as f:
    variant = f.read()


for r in range(2, 31):
    indeces = 0
    for i in range(0, r):
        block = "".join([variant[i] for i in range(i, len(variant) - r + 1, r)])
        indeces += index_of_coincidence(block)
    index_value = indeces / r
    print(f"Індекс відповідності для блоків довжини {r}: {index_value}")


print("\nМожливий ключ:", find_key(15, variant))


right_key = 'крадущийсявтени'
plain_variant = vig_dec(variant, right_key)
print(f"\nПравильний ключ: {right_key}\n\n{plain_variant}")


with open('plain_variant.txt', 'w', encoding="utf-8") as f:
    f.write(plain_variant)
