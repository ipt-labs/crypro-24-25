import matplotlib.pyplot as plt

ciphered = '3text.txt'
all_chars = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
result = 'result.txt'

def blocks(data, len_key):
    return [data[i::len_key] for i in range(len_key)]

def index(data):
    n = len(data)
    freq = {char: data.count(char) for char in set(data)}
    sum_of = sum(count * (count - 1) for count in freq.values())
    return sum_of / (n * (n - 1)) if n > 1 else 0

def index_for_key(list_blocks):
    return sum(index(block) for block in list_blocks) / len(list_blocks)

def key_len_index(text):
    key_index = {k: index_for_key(blocks(text, k)) for k in range(2, 31)}
    return key_index

def decryption(data, key):
    deciphered_data = ''
    for i, el in enumerate(data):
        d_index = all_chars.index(el)
        k_index = all_chars.index(key[i % len(key)])
        new_i_index = (d_index - k_index) % len(all_chars)
        deciphered_data += all_chars[new_i_index]
    return deciphered_data

with open(ciphered, 'r', encoding='utf-8') as t:
    cphrd_text = t.read().replace('\n', '')


res = key_len_index(cphrd_text)
len_my_key = max(res, key=res.get)
print('Довжина ключа: ', len_my_key)


plt.scatter(res.keys(), res.values())
plt.xticks(range(len(res) + 2), range(len(res) + 2))
plt.xlabel("Довжина ключа")
plt.ylabel("Індекс")
plt.title("Індекс відповідності для різних довжин ключа")
plt.show()

def my_key(data, len_key):
    most_often_letters = 'оеаи'
    
    for a in most_often_letters:
        key_letters = ''
        blcks = blocks(data, len_key)

        most_common = {}
        for b in blcks:
            freq = {ltr: b.count(ltr) for ltr in set(b)}
            most_common_letter = max(freq, key=freq.get)
            most_common[blcks.index(b) + 1] = most_common_letter

        for v in most_common.values():
            o_index = all_chars.index(a)
            v_index = all_chars.index(v)
            k_index = (v_index - o_index) % len(all_chars)
            key_letters += all_chars[k_index]

        print(a, key_letters)


my_key(cphrd_text, len_my_key)

key = "арудазовархимаг"

res_7 = decryption(cphrd_text, key)
print("Розшифрований текст: ", res_7)

with open(result, 'w', encoding='utf-8') as ws:
    ws.write(res_7)
