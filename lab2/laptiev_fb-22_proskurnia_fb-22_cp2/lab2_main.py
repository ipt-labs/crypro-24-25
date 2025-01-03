import random
from collections import Counter




R2_KEY = 'бу'
R3_KEY = 'дай'
R4_KEY = 'грут'
R5_KEY = 'бринь'
R18_KEY = 'сравпесзгорилахата'
M = 32
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"




def prep_text(path):
    file = open(path, "r", encoding="utf-8")
    text = file.read()
    text = text.lower()
    text = ''.join(filter(lambda char: char in set(ALPHABET), text))
    text = text.replace('ё', 'е')

    # with open('filtered_text.txt', "w", encoding="utf-8") as file:
    #         file.write(text)

    return text


def random_keys():
    return [''.join(random.choices(ALPHABET, k=i)) for i in range(1, 31)]
     

def AffinityIndex(text):
    symbols = Counter(text)

    _sum = 0
    for count in symbols.values():
        _sum += count * (count - 1)

    return _sum / (sum(symbols.values()) * (sum(symbols.values()) - 1))


def count_repeated_letters(text, r):
    count = 0
    for i in range(len(text) - r):
        if text[i] == text[i + r]:
            count += 1
    return count


def vigenere_encrypt(text, key):
    encrypted_text = ''
    key_length = len(key)
    indexed_key = [ALPHABET.index(i) for i in key]
    indexed_text = [ALPHABET.index(i) for i in text]
    
    for i in range(len(indexed_text)):
        index = (indexed_text[i] + indexed_key[i % key_length]) % len(ALPHABET)
        encrypted_text += ALPHABET[index]
    
    return encrypted_text


def freq(text):
    freq_s = Counter(text)
    length = len(text)
    for i, j in freq_s.items():
        freq_s[i] = j / length
    return freq_s


def decrypt(c, k) -> str:
    i = (ALPHABET.find(c) - ALPHABET.find(k)) % len(ALPHABET)
    return ALPHABET[i]    


def vigenere_decrypt(text, key):
    decrypted_text = ''
    key_length = len(key)
    key_as_int = [ALPHABET.index(i) for i in key]
    text_as_int = [ALPHABET.index(i) for i in text]
    
    for i in range(len(text_as_int)):
        value = (text_as_int[i] - key_as_int[i % key_length]) % len(ALPHABET)
        decrypted_text += ALPHABET[value]
    
    return decrypted_text




def main():
    plain_text = prep_text('text.txt')
    print('I0', 1/M)
    print('I(plain text)', AffinityIndex(plain_text))
    for key in random_keys():
        cipher_text = vigenere_encrypt(plain_text, key)
        print(f'r{len(key)}: ', AffinityIndex(cipher_text))
    



    print('///////////////////////////////_analyzing_///////////////////////////////')
    cipher_text = prep_text('var_text.txt')

    indexes = {}
    collision_counts={}
    for i in range(1, 31):
        index = AffinityIndex(cipher_text[::i])
        indexes[i] = index
        print(f'r{i} ',index)

        col_count = count_repeated_letters(cipher_text, i)
        collision_counts[i] = col_count
        print('collision count', col_count, '\n')

    print('Top 5 indexes: ', dict(sorted(indexes.items(), key=lambda item: item[1], reverse=True)[:5]))
    print('Top 5 collision counts:', dict(sorted(collision_counts.items(), key=lambda item: item[1], reverse=True)[:5]))
    
    print('o frequency:', freq(cipher_text)['о'])

    key_len = 16
    for i in range(key_len):
        freq_s = freq(cipher_text[i::key_len])
        print(f"Letter {i}:", dict(sorted(freq_s.items(), key=lambda item: item[1], reverse=True)[:5]))


    # keyfrag = ['тй', 'ут', 'шрщ', 'уцьо', 'щрл', 'цнрх', 'яцюс', 'ьу', 'пйж', 'ьуо', 'юбх', 'ь', 'чаъ', 'тын', 'у', 'чсо'] # freq > 0.079
    # keyfrag = ['тй', 'ут', 'шрщ', 'уцьо', 'щрл', 'цнрх', 'я', 'ь', 'п', 'ь', 'ю', 'ь', 'чаъ', 'тын', 'у', 'чсо'] # with собор
    # keyfrag = ['т', 'у', 'шрщ', 'уцьо', 'щрл', 'цнрх', 'я', 'ь', 'п', 'ь', 'ю', 'ь', 'чаъ', 'тын', 'у', 'чсо'] # without ддк & lower
    # keyfrag = ['т', 'у', 'шрщ', 'уцьо', 'щрл', 'цнрх', 'яцюс', 'ь', 'п', 'ь', 'ю', 'ь', 'а', 'ы', 'у', 'ч'] # with оборотней
    # keyfrag = ['т', 'у', 'щ', 'уцьо', 'щрл', 'цнрх', 'яцюс', 'ь', 'п', 'ь', 'ю', 'ь', 'а', 'ы', 'у', 'ч'] # with дел
    keyfrag = ['т', 'у', 'щ', 'цьо', 'щрл', 'цнрх', 'яцюс', 'ь', 'п', 'ь', 'ю', 'ь', 'а', 'ы', 'у', 'ч'] # without делe


    with open("keys.txt", "w", encoding='utf-8') as f:
        def reqout(part, symbols):
            if len(part) >= 16:
                f.write(part + '\n')
                return
            mb = symbols[:1][0]
            for i in mb:
                i = decrypt(i, 'о')
                reqout(part+i, symbols[1:])
        reqout("", keyfrag)

    with open("de_text.txt", "w", encoding='utf-8') as f:
        key = 'делолисоборотней'
        f.write(vigenere_decrypt(cipher_text, key))
    
    


if __name__ == "__main__":
    main()