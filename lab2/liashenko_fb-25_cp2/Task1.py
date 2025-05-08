import string

def vigenere_encrypt(text, key, alphabet):
    encrypted_text = []
    key_length = len(key)
    key_indices = [alphabet.index(k) for k in key]
    
    for i, char in enumerate(text):
        if char in alphabet:
            text_index = alphabet.index(char)
            key_index = key_indices[i % key_length]
            encrypted_char = alphabet[(text_index + key_index) % len(alphabet)]
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    
    return ''.join(encrypted_text)

def main():
    russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    
    keys = {
        2: "из",
        3: "тот",
        4: "него",
        5: "перед",
        14: "замешательстве",
        18: "сверхъестественных"
    }
    
    input_file = 'text1.txt'
    with open(input_file, 'r', encoding='utf-8') as f:
        plaintext = f.read().lower()
    
    filtered_text = ''.join([char for char in plaintext if char in russian_alphabet])
    
    for key_length, key in keys.items():
        encrypted_text = vigenere_encrypt(filtered_text, key, russian_alphabet)
        output_file = f'encrypted_r{key_length}.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_text)
        print(f'Text encrypted with key length {key_length} and saved to file {output_file}')

if __name__ == "__main__":
    main()
