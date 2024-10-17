import matplotlib.pyplot as plt
import math
import csv

alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

def get_letter_frequency(file_name):
    frequency = dict()
    with open(file_name, "r") as file:
        csvText = list(csv.reader(file))
        for i in range(1, len(csvText) - 1):
            item = csvText[i][0].split(";")
            frequency[item[0]] = float(item[1])

    return frequency

def filter_text(text):
    filter_symb = ["\n", " "]

    for item in filter_symb:
        text = text.replace(item, "")
    
    return text

def make_bloks(text, r):
    lst = list()
    for i in range(r):
        word = ""
        for j in range(i, len(text), r):
            word += text[j]
        lst.append(word)
    
    return lst

def symbols_count(text):
    symbols = dict()
    for item in text:
        if item not in symbols.keys():
            symbols[item] = 1
        else:
            symbols[item] += 1

    return symbols

def block_symb_len(lst):
    lett_lst = []
    for i in range(len(lst)):
        lett_lst.append(symbols_count(lst[i]))
    
    return lett_lst

def calculate_index(text, r):
    lst = make_bloks(text, r)
    lett_lst = block_symb_len(lst)

    y_lst = []
    for item in lett_lst:
        res_sum = 0
        for count in item.values():
            res_sum += count * (count - 1)
        gen_sum = sum(list(item.values()))
        y_lst.append(1/(gen_sum * (gen_sum - 1)) * res_sum)

    return sum(y_lst) / len(y_lst)

def get_key(text, r):
    lst = make_bloks(text, r)
    lett_lst = block_symb_len(lst)

    final_dict = []
    for item in lett_lst:
        final_dict.append(dict([max(item.items(), key=lambda kv: kv[1])]))

    key_val = []
    for item in final_dict:
        key_val.append((alph.index(list(item.keys())[0]) - alph.index("о")) % len(alph))

    return ''.join(alph[item] for item in key_val)

def calc_theor_val():
    freq = get_letter_frequency("Table1_freq.csv")

    res_sum = 0
    for item in freq.values():
        res_sum += item ** 2
    
    return res_sum

def find_key_len(index_val):
    theor_index = calc_theor_val()

    key_len = []
    for i in range(len(index_val)):
        if math.isclose(index_val[i], theor_index, abs_tol=0.005):
            key_len.append(i + 2)

    return key_len[0]

def decode_text(text, key):
    dec_text = ""
    for i in range(len(text)):
        dec_text += alph[alph.index(text[i]) - alph.index(key[i % len(key)])]
    return dec_text

def main():
    text = ""
    with open("text.txt", "r", encoding = "utf-8") as file:
        text = file.read()
    
    text = filter_text(text)

    index_val = []
    for i in range(2, 31):
        index_val.append(calculate_index(text, i))

    print("*** Index of Coincidence ***\n" + "-" * 30)
    for i in range(len(index_val)):
        print(f"{i + 2}: {index_val[i]}")
    print()

    print("*** Theoretical value of I ***\n" + "-" * 30)
    print(calc_theor_val(), "\n")

    key_len = find_key_len(index_val)
    key = get_key(text, key_len)
    print("*** Found key ***\n" + "-" * 30)
    print(key, "\n")

    key = "вшекспирбуря"
    print("*** Real key ***\n" + "-" * 30)
    print(key, "\n")

    dec_text = decode_text(text, key)
    print(f"*** Decoded text ***\n" + "-" * 30)
    print(dec_text, "\n")

    # Plot
    plt.plot(index_val)
    plt.xlabel('Довжина ключа')
    plt.ylabel('Індекс відповідності')
    plt.show()

if __name__ == "__main__":
    main()