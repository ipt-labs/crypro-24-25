from math import gcd

#Розширений алгоритм Евкліда
def euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = euclid(b % a, a)
        return g, y - (b // a) * x, x

#Розв'язання лінійних порівнянь
def linear_solve(a, b, mod):
    g = gcd(a, mod)
    if b % g != 0:
        return None
    x0 = (euclid(a // g, mod // g)[1] * (b // g)) % (mod // g)
    return [x0 + i * (mod // g) for i in range(g)]

def decrypt(text, key, symbol):
    res = ""
    mod = len(symbol) ** 2
    for i in range(0, len(text), 2):
        y = symbol.index(text[i]) * len(symbol) + symbol.index(text[i+1])
        x = (euclid(key[0], mod)[1] * (y - key[1])) % mod
        res += symbol[x // len(symbol)] + symbol[x % len(symbol)]
    return res

#Визначення ключа та розшифрування тексту
def key_decrypt(text, freq_bigr, top_5_bigram, symbol):
    mod = len(symbol) ** 2
    candidates = []
    for normal in freq_bigr:
        for encrypted in top_5_bigram:
            x1, y1 = symbol.index(normal[0]) * len(symbol) + symbol.index(normal[1]), \
                     symbol.index(encrypted[0]) * len(symbol) + symbol.index(encrypted[1])
            for normal2 in freq_bigr:
                for encrypted2 in top_5_bigram:
                    if normal != normal2 and encrypted != encrypted2:
                        x2, y2 = symbol.index(normal2[0]) * len(symbol) + symbol.index(normal2[1]), \
                                 symbol.index(encrypted2[0]) * len(symbol) + symbol.index(encrypted2[1])
                        roots = linear_solve(x1 - x2, y1 - y2, mod)
                        if roots:
                            for a in roots:
                                b = (y1 - a * x1) % mod
                                decrypted = decrypt(text, (a, b), symbol)
                                if all(bigram not in decrypted for bigram in ['аь', 'еь', 'юы', 'яы', 'эы', 'юь',
                                                                              'яь', 'оь', 'иь', 'ыь', 'уь', 'аы',
                                                                              'эь', 'ць', 'хь', 'кь', 'оы', 'иы',
                                                                              'ыы', 'уы', 'еы']):
                                    candidates.append(((a, b), decrypted))
    if candidates:
        return candidates[0][1], candidates[0][0]
    return None, None

#Аналіз біграм у тексті
def analyse_bigr(file_path, alphabet):
    bigr = {i + j: 0 for i in alphabet for j in alphabet}
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', '').lower()
    text_leng = len(text)
    for i in range(0, text_leng - 1, 2):
        bigram = text[i:i+2]
        if bigram in bigr:
            bigr[bigram] += 1
    return sorted(bigr.items(), key=lambda item: item[1], reverse=True)[:5]

def main(file_path):
    symbol = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    freq_bigr = ['ст', 'но', 'то', 'на', 'ен']
    top_5_bigram = [bigram[0] for bigram in analyse_bigr(file_path, symbol)]

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', '')

    print("Приклади роботи функцій")
    g, x, y = euclid(30, 18)
    print(f"Розширений алгоритм Евкліда для 30 і 18: НСД = {g}")

    solution = linear_solve(14, 30, 100)
    print(f"Лінійне порівняння 14x ≡ 30 (mod 100): Розв'язок = {solution}")

    print("-----")
    print("Найчастіші біграми")
    print(f"Топ-5 біграм у тексті: {top_5_bigram}")

    decrypted_text, key = key_decrypt(text, freq_bigr, top_5_bigram, symbol)
    if decrypted_text:
        print("-----")
        print("Результати розшифрування:")
        print(f"Розшифрований текст (перші 100 символів): {decrypted_text[:100]}")
        print(f"Знайдений ключ: {key}")
    else:
        print("Не вдалося розшифрувати текст.")

main('08.txt')