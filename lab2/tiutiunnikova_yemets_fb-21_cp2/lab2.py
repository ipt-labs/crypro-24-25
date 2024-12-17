import string
from collections import Counter
import openpyxl
import matplotlib.pyplot as plt

#----ФІЛЬТРАЦІЯ----
def filt(txt):
    txt = txt.lower().replace('ё', 'е')
    return ''.join(filter(lambda c: c in string.ascii_lowercase + 'абвгдежзийклмнопрстуфхцчшщъыьэюя', txt))

#----ШИФРУВАННЯ----
def encrypt(plain, key):
    cipher = []
    key_len = len(key)
    key_offsets = [ord(c) - ord('а') for c in key]
    text_offsets = [ord(c) - ord('а') for c in plain]

    for i in range(len(text_offsets)):
        offset = (text_offsets[i] + key_offsets[i % key_len]) % 32
        cipher.append(chr(offset + ord('а')))
    
    return ''.join(cipher)

#----ІНДЕКСИ----
def calc_idx(txt):
    n = len(txt)
    freq = Counter(txt)
    idx = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return idx

#----ЗБЕРЕЖЕННЯ ТАБЛИЦІ----
def save_tbl(data, fname):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Індекси відповідності"
    ws.append(["Ключ", "Довжина", "Індекс", "Різниця з оригіналом"])
    for row in data:
        ws.append(row)
    wb.save(fname)

#----ЗБЕРЕЖЕННЯ ЗАШИФР. ФАЙЛУ----
def save_enc(enc_data, fname):
    with open(fname, "w", encoding="utf-8") as f:
        for key, txt in enc_data:
            f.write(f"Ключ: {key}\n")
            f.write(f"{txt}\n\n")

#----КЛЮЧ----
def gen_key(len_key):
    keys = {
        2: "мы",
        3: "дом",
        4: "лего",
        5: "зверь",
        10: "пенекветка",
        11: "вдохновение",
        12: "авиаработник",
        13: "контрразведка",
        14: "активизировать",
        15: "оппозиционность",
        16: "специализируемый",
        17: "легкомысленничать",
        18: "экспериментировать",
        19: "неудовлетворительно",
        20: "гипертрофированность"
    }
    return keys.get(len_key, "")

#----ГРАФІК----
def grafic(key_lens, idxs, orig_idx):
    plt.scatter(key_lens, idxs, color='b')
    plt.xlabel('Довжина ключа')
    plt.ylabel('Індекс відповідності')
    plt.legend()
    plt.grid()
    plt.show()

#---------------------------------------------------------------------------
fname = "original_text.txt"
with open(fname, "r", encoding="utf-8") as f:
    txt = f.read()

txt = filt(txt)

key_lens = [2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
data = []

start_index = calc_idx(txt)
index_list = []
encrypted_pairs = []

for l in key_lens:
    key = gen_key(l)
    enc_txt = encrypt(txt, key)
    enc_idx = calc_idx(enc_txt)
    diff = abs(start_index - enc_idx)
    data.append([key, l, enc_idx, diff])
    encrypted_pairs.append((key, enc_txt))
    index_list.append(enc_idx)
    print(f"Довжина ключа: {l} | Індекс: {enc_idx:.5f} | Різниця: {diff:.5f}")

print(f"\nІндекс початкового тексту: {start_index:.5f}")
save_tbl(data, "indexes.xlsx")
save_enc(encrypted_pairs, "encrypted.txt")
grafic(key_lens, index_list, start_index)
