import re

# ----ФІЛЬТРАЦІЯ----
def clean(txt):
    txt = txt.lower()
    txt = txt.replace('ё', 'е')
    txt = re.sub(r'[^абвгдежзийклмнопрстуфхцчшщъыьэюя]', '', txt)
    return txt

# ----РОЗШИФРУВАННЯ----
def decode(cipher, key):
    alpha = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    result = []
    key_idx = [alpha.index(c) for c in key]
    cipher_idx = []

    for c in cipher:
        if c in alpha:  
            cipher_idx.append(alpha.index(c))
        else:
            cipher_idx.append(None)

    for i in range(len(cipher_idx)):
        if cipher_idx[i] is not None: 
            value = (cipher_idx[i] - key_idx[i % len(key)]) % len(alpha)
            result.append(alpha[value])
        else:
            result.append(cipher[i])

    return ''.join(result)

# ----ЗЧИТУВАННЯ -------
def read(path):
    with open(path, "r", encoding='utf-8') as f:
        return f.read().strip()

# -----------------------
filepath = "task3.txt" 
key = "делолисоборотней" 

ciphertext = read(filepath) 
cleaned = clean(ciphertext) 
decoded = decode(cleaned, key)  
print("Розшифрований текст:", decoded)
