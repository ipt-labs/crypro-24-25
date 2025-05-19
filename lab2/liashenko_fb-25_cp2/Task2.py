import string
import matplotlib.pyplot as plt

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
    
    return ''.join(encrypted_text)

def calculate_index_of_coincidence(text, alphabet):
    frequencies = [text.count(char) for char in alphabet]
    text_length = len(text)
    numerator = sum(f * (f - 1) for f in frequencies)
    denominator = text_length * (text_length - 1)
    return numerator / denominator if denominator != 0 else 0

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
    
    ic_plaintext = calculate_index_of_coincidence(filtered_text, russian_alphabet)
    print(f"Index of visibility of the hidden text: {ic_plaintext}")
    
    ic_values = {"Відкритий текст": ic_plaintext}
    
    for key_length, key in keys.items():
        encrypted_text = vigenere_encrypt(filtered_text, key, russian_alphabet)
        output_file = f'encrypted_r{key_length}.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_text)
        
        ic_encrypted = calculate_index_of_coincidence(encrypted_text, russian_alphabet)
        ic_values[f"r {key_length}"] = ic_encrypted
        print(f"Match index for key length {key_length}: {ic_encrypted}")
    
    plt.figure(figsize=(10, 6))
    labels = list(ic_values.keys())
    values = list(ic_values.values())
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Тип тексту')
    plt.ylabel('Індекс відповідності')
    plt.title('Індекси відповідності ')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('index_of_coincidence_chart.png')
    plt.show()

if __name__ == "__main__":
    main()
