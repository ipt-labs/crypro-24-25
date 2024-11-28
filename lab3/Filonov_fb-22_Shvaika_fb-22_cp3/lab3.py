from argparse import ArgumentParser
from collections import Counter
from re import sub


def nsd_calc(num_1, num_2):  
    if not num_2:  
        return num_1, 1, 0 
    nsd, val1, val2 = nsd_calc(num_2, divmod(num_1, num_2)[1])  
    x, y = val2, val1 - divmod(num_1, num_2)[0] * val2 
    return nsd, x, y 
 

def congruence(a, b, m): 
    nsd_res, x, _ = nsd_calc(a, m) 
     
    if b % nsd_res != 0: 
        return None 
     
    a, b, m = a // nsd_res, b // nsd_res, m // nsd_res  
    x1 = (x * b) % m  
    result = [(x1 + i * m) % (m * nsd_res) for i in range(nsd_res)] 
    return result


def txt_formatting(text):
    with open(text, 'r') as file: 
        text = file.read().lower()
        text = sub(r'[^а-яё ]', ' ', text) 
        text = text.replace(' ', '')

    return text


def frequency(sum, total): 
    freq = {} 
    for value in sum: 
        freq[value] = sum[value] / total 
 
    return freq 


def bigrams_freq(text): 
    bigrams = [text[i:i + 2] for i in range(0, len(text))] 
    bigram_counts = Counter(bigrams) 
    total_bigrams = len(bigrams)  
    freq = frequency(bigram_counts, total_bigrams) 
    freq = sorted(freq, key=freq.get, reverse=True) 
    return freq[:5] 


def monograms_freq(text): 
    monogram_counts = Counter(text) 
    total_letters = sum(monogram_counts.values()) 
    freq = frequency(monogram_counts, total_letters) 
    freq = sorted(freq, key=freq.get, reverse=True) 
    return freq  


def find_keys(bigrams, top_bigrams, alphabet): 
    keys = [] 
    for i in range(len(bigrams)-1): 
        for j in range(i+1, len(bigrams)): 
            for k in range(len(top_bigrams)): 
                for f in range(len(top_bigrams)): 
                    if k==f: continue 
                    x1 = alphabet.index(top_bigrams[k][0])*31 + alphabet.index(top_bigrams[k][1]) 
                    x2 = alphabet.index(top_bigrams[f][0])*31 + alphabet.index(top_bigrams[f][1]) 
                    y1 = alphabet.index(bigrams[i][0])*31 + alphabet.index(bigrams[i][1]) 
                    y2 = alphabet.index(bigrams[j][0])*31 + alphabet.index(bigrams[j][1]) 
                    a = congruence(x1-x2, y1-y2, 31**2) 
                    if a != None: 
                        for l in range(len(a)): 
                            keys.append([a[l], (y1-a[l]*x1)%(31**2)]) 
    return keys 
 

def decrypt_text(text, a, b, alphabet): 
    bigrams = [text[i:i+2] for i in range(0, len(text), 2)] 
    _, a, _ = nsd_calc(a, 31**2) 
    for i in range(len(bigrams)): 
        bg = '' 
        y = alphabet.index(bigrams[i][0])*31 + alphabet.index(bigrams[i][1]) 
        x = ((y - b)*(a%31**2))%31**2 
        bg += alphabet[x//31] 
        bg += alphabet[x%31] 
        bigrams[i] = bg 
    return ''.join(bigrams) 
 

def find_correct_key(text, keys, alphabet, dec_path_storage): 
    for i in range(len(keys)): 
        decrypted_text = decrypt_text(text, keys[i][0], keys[i][1], alphabet) 
        mn_freq = monograms_freq(decrypted_text) 
        mn_freq_hight = mn_freq[:5] 
        mn_freq_low = mn_freq[5:] 
        if 'о' in mn_freq_hight and 'е' in mn_freq_hight and 'а' in mn_freq_hight: 
            if 'ф' in mn_freq_low and 'щ' in mn_freq_low: 
                if 'аь' not in decrypted_text: 
                    print(f'знайдено ключі a={keys[i][0]}, b={keys[i][1]}') 
                    with open(dec_path_storage, 'w') as file: 
                        file.write(f'a={keys[i][0]}, b={keys[i][1]} \n{decrypted_text}') 
 
 
def init():
    arg_parser = ArgumentParser(
        prog='Програма для лабораторної роботи №3. Виконали студенти групи ФБ-22 Швайка та Філонов',
        description='Код містить підпрограми необхідні для розшифрування тексту та перебирає усі можливі біграми, щоб знайти ключі для дешифрування'
    )
    arg_parser.add_argument('file')
    arg_parser.add_argument('dec_file_res')
    args = arg_parser.parse_args()
 
    text = txt_formatting(args.file)
    bigram = bigrams_freq(text)
    print(f'''5 найчастіших біграм:
        1. {bigram[0]}
        2. {bigram[1]}
        3. {bigram[2]}
        4. {bigram[3]}
        5. {bigram[4]}
    ''')

    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    top_bigrams = ['ст', 'но', 'то', 'на', 'ен'] 
    keys_val = find_keys(bigram, top_bigrams, alphabet)
    find_correct_key(text, keys_val, alphabet, args.dec_file_res)
 

init()
