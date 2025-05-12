import re
from collections import Counter
import matplotlib.pyplot as plt

#1-2
def vigenere_encrypt(plain_text, key):
    encrypted_text = ""
    key_repeated = (key * (len(plain_text) // len(key))) + key[:len(plain_text) % len(key)]

    for i in range(len(plain_text)):
        shift = ord(key_repeated[i].lower()) - ord('а')
        encrypted_char = chr((ord(plain_text[i].lower()) - ord('а') + shift) % 32 + ord('а'))
        encrypted_text += encrypted_char

    return encrypted_text

def index_of_coincidence(block):
    n = len(block)
    frequencies = Counter(block)
    ic = sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

def replace(continious_text):
    clean = ''
    continious_text = continious_text.replace('ё', 'е')
    for i in continious_text:
        if i in alphabet:
            clean += i
    return clean


file = open('letov', encoding ='utf-8')
text = file.read()

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
la = len(alphabet) # 32

text = re.sub(r'[^а-яА-ЯёЁ]', '', text)
text = text.lower()

keys = ["не", "квн", "душа", "еврей", 
        "йосифвольф", "матвейгофман", "хирургпрезидент", 
        "подполковникладкин", "цадикифрадковэтоодин"]
encrypted_texts = []

for key in keys:
    encrypted_text = vigenere_encrypt(text, key)
    encrypted_texts.append(encrypted_text)

open_text_ic = index_of_coincidence(text)

encrypted_texts_ic = [index_of_coincidence(text) for text in encrypted_texts]

print(f"Original text:\n{text}")
for i in range(len(keys)):
    print(f"\nEncrypted text with {keys[i]}:\n{encrypted_texts[i]}")

print(f"Index of coincidence for open text:\n{open_text_ic}:.4f")
for i in range(len(keys)):
    print(f"Index of coincidence for encrypted text with {keys[i]}:\n{encrypted_texts_ic[i]:.4f}")


plt.figure(figsize=(8, 5))
text_types = ['0'] + [f'r{len(key)}' for key in keys]
ics = [open_text_ic] + encrypted_texts_ic
plt.bar(text_types, ics, color=['blue'] + ['green']*len(keys))
plt.title('Index of coincidence comparison')
plt.xlabel('')
plt.ylabel('Index of coincidence')
plt.ylim(0, 0.06)
plt.show()

#3
def vigenere_decrypt(cipher_nums, key_nums):     
    return [(c - k) % la for c, k in zip(cipher_nums, key_nums * (len(cipher_nums) // len(key_nums) + 1))]


def to_nums(text):
    nums = [alphabet.index(i) for i in text]
    return nums

def from_nums(nums):
    text = ''.join(alphabet[i] for i in nums)
    return text

def find_period(ciphertext, max_r=32):
    ic_values = []
    for r in range(2, max_r + 1):
        blocks = [ciphertext[i::r] for i in range(r)]
        ic = sum(index_of_coincidence(block) for block in blocks) / r
        ic_values.append(ic)
    best_r = ic_values.index(max(ic_values)) + 2
    return best_r, ic_values

def get_key(ciphertext, r):
    blocks = [ciphertext[i::r] for i in range(r)]
    key = ''
    for block in blocks:
        most_common = Counter(block).most_common(1)[0][0]
        key_char = alphabet[(alphabet.index(most_common) - alphabet.index('о')) % la]
        key += key_char
    return key

def coincidences(text, r):
    d = 0
    for i in range(len(text) - r):
        if text[i] == text[i + r]:
            d += 1
    return d

file2 = open('variant11', encoding ='utf-8')
ciphertext= file2.read()
ciphertext = replace(ciphertext)

print('\nTask3\n')
D = []

for i in range(2, 32):
    D.append(coincidences(ciphertext, i))
    print('r =', i, 'D =', D[i - 2])
period = D.index(max(D)) + 2

key = get_key(ciphertext, period)
print(f"Key: {key}")
#'пецвенецианскийку'

decrypted_text = from_nums(vigenere_decrypt(to_nums(ciphertext), to_nums(key)))
print('Decrypted text with key:')
print(decrypted_text)

r_values = list(range(2, 32))
coincidence_values = D

max_D = max(coincidence_values)
max_index = coincidence_values.index(max_D)

colors = ['blue'] * len(coincidence_values)
colors[max_index] = 'red' 

plt.bar(r_values, coincidence_values, color=colors, alpha=0.7)
plt.title('')
plt.xlabel('r')
plt.ylabel('Coincidence index')
plt.show()
    
