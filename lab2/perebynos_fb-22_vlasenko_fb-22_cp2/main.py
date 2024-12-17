import random
from tabulate import tabulate


ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
MOST_FREQUENT_SYMBOL = "о"


# encrypt one symbol using Caesar cipher
def encrypt(m, k) -> str:
    i = (ALPHABET.find(m) + ALPHABET.find(k)) % len(ALPHABET)
    return ALPHABET[i]


# encrypt text using keystream (stream of character)
# Useful for encrypt with Vigenere cipher
def encrypt_stream(pt: str, stream_key) -> str:
    ct = ""
    for m in pt:
        ct += encrypt(m, stream_key.next())

    return ct


# decrypt one symbol using Caesar cipher
def decrypt(c, k) -> str:
    i = (ALPHABET.find(c) - ALPHABET.find(k)) % len(ALPHABET)
    return ALPHABET[i]


# decrypt text using keystream (stream of character)
# Useful for decrypt with Vigenere cipher
def decrypt_stream(ct: str, stream_key) -> str:
    pt = ""
    for c in ct:
        pt += decrypt(c, stream_key.next())
        
    return pt


# Index of coincidence
# Indicates how evenly the characters
# are distributed in the language
def ic(text: str) -> float:
    alph = {i: 0 for i in ALPHABET}
    for i in text:
        if i not in ALPHABET:
            raise Exception("Invalid letter")

        alph[i] += 1

    summ = 0
    for v in alph.values():
        summ += v * (v - 1)

    return summ / (sum(alph.values()) * (sum(alph.values())-1)) 


# Used for find sum of Kronecker symbols over all text
# for specified distance between letters
def colision_stat(text: str, r: int) -> int:
    stat = 0
    for i in range(len(text)-r):
        if text[i] == text[i+r]:
            stat += 1
    return stat


# lowerize text and remove all
# non alpha character, whitespace
# not included in prepared text
def prepare_text(text: str) -> str:
    out = ""
    for i in text:
        if i.lower() not in ALPHABET:
            continue

        out += i.lower()

    return out


# calculate symbol frequencies in text
def frequencies(text: str) -> dict[str, float]:
    freq = {i: 0 for i in ALPHABET}
    for i in text:
        if i not in ALPHABET:
            raise Exception("Invalid letter")

        freq[i] += 1

    count = sum(freq.values())
    for k in freq:
        freq[k] /= count

    return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))


# class that used for generate keystream
# for encrypting with vigenere cipher
class VigenereKeyStream:
    key: str
    key_len: int
    offset: int = 0

    def __init__(self, key: str):
        for i in key:
            if i not in ALPHABET:
                raise Exception("Invalid key")
        
        self.key = key
        self.key_len = len(key)

    # reset offset for reusing 
    # existed key
    def reset(self):
        self.offset = 0

    # produce next symbol from key
    def next(self) -> str:
        s = self.key[self.offset]
        self.offset = (self.offset + 1) % self.key_len
        return s


def main():

    keys = ["а", "вы", "дуб", "ночь", "огонь", "вопрос", "медведь", "мельница", "организмы", "предложить", "преподавать", "исследовать", "неопределенность", "профессионально", "непредсказуемость", "систематизированный"]
    keys = ["".join(random.choices(ALPHABET, k=i)) for i in range(1, 31)]


    text = ""
    with open("texts/pt.txt", "r") as f:
        text = f.read()
    pt = prepare_text(text)
    
    print("IC0:", 1/len(ALPHABET))

    print("IC(pt):", ic(pt))
    print("IC for plaintext encrypted by keys of different length")
    ptctr = []
    for i in keys:
        ks = VigenereKeyStream(i)
        ct = encrypt_stream(pt, ks)
        ptctr.append(f"IC(ct r={len(i)}): {ic(ct)}")
    
    print(tabulate([ptctr[i:i+3] for i in range(0, len(ptctr), 3)], headers=["", "", ""]))
    print()
    text = ""
    with open("texts/2_ct.txt", "r") as f:
        text = f.read()
    ct = prepare_text(text)


    print("IC(ct):", ic(ct))
    ctic = []
    ctcs = []
    for i in range(1, 31):
        ctic.append(f"CS(ct r={i}): {colision_stat(ct, i)}")
        ctcs.append(f"IC(ct r={i}): {ic(ct[::i])}")

    print("IC for cipher text with different length of key")
    print(tabulate([ctic[i:i+3] for i in range(0, len(ctic), 3)], headers=["", "", ""]))
    print("\nSum of Kroneker symbol for differen length of key")
    print(tabulate([ctcs[i:i+3] for i in range(0, len(ctcs), 3)], headers=["", "", ""]))

    print()
    print("Letters frequency for every key symbol")
    key_len = 14
    for i in range(key_len):
        freq = frequencies(ct[i::key_len])
        print(f"Letter {i}:", list(freq.items())[:5])
    
    print()

    # save probably correct keys in file
    with open("texts/keys.txt", "w") as f:
        keyfrag = ["фэ", "ьу", "яц", "рлщ", "ук", "йт", "ты", "цин", "ч", "тд", "ьу", "х", "ьу", "ю"]
        def reqout(part, symbols):
            if len(part) >= 14:
                f.write(part + "\n")
                return
            mb = symbols[:1][0]
            for i in mb:
                i = decrypt(i, MOST_FREQUENT_SYMBOL)
                reqout(part+i, symbols[1:])
        reqout("", keyfrag)
    
    print("Key:", "последнийдозор")
    # decrypt and save plaintext in file
    ks = VigenereKeyStream("последнийдозор")
    with open("texts/2_pt.txt", "w") as f:
        f.write(decrypt_stream(ct, ks))


if __name__=="__main__":
    main()
