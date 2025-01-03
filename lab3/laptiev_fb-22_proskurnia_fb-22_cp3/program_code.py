from itertools import permutations

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alphabet)  # 31

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', '')

#програма із алгоритмом Евкліда
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def find_inverse(a, mod):
    gcd, x, _ = gcd_extended(a, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    return -1
    
def solve_equation(a, b, mod):
    gcd, x, _ = gcd_extended(a, mod)
    if gcd == 1:
        return (find_inverse(a, mod) * b) % mod
    if b % gcd != 0:
        return -1
    a1, b1, n1 = a // gcd, b // gcd, mod // gcd
    x0 = solve_equation(a1, b1, n1)
    return int(x0)

def bigram_to_num(bigram):
    return alphabet.index(bigram[0]) * m + alphabet.index(bigram[1])

def num_to_bigram(num):
    return alphabet[num // m] + alphabet[num % m]

def encrypt_bigram(a, b, bigram):
    x = bigram_to_num(bigram)
    y = (a * x + b) % (m * m)
    return num_to_bigram(y)

def decrypt_bigram(a, b, bigram):
    y = bigram_to_num(bigram)
    x = (find_inverse(a, m * m) * (y - b)) % (m * m)
    return num_to_bigram(x)

def encrypt_text(a, b, text):
    bigrams = [text[i:i + 2] for i in range(0, len(text), 2)]
    return ''.join(encrypt_bigram(a, b, bigram) for bigram in bigrams)

# Розшифрування тексту з перевіркою змістовності
def decrypt_text(a, b, text):
    bigrams = [text[i:i + 2] for i in range(0, len(text), 2)]
    decrypted = ''.join(decrypt_bigram(a, b, bigram) for bigram in bigrams)
    if decrypted.count('о') / len(decrypted) < 0.11 or decrypted.count('а') / len(decrypted) < 0.07:
        return -1
    return decrypted

def generate_keys(open_bigrams, encrypted_bigrams):
    open_pairs = list(permutations(open_bigrams, 2))
    encrypted_pairs = list(permutations(encrypted_bigrams, 2))
    keys = []
    for (x1, x2), (y1, y2) in zip(open_pairs, encrypted_pairs):
        y_diff = bigram_to_num(y1) - bigram_to_num(y2)
        x_diff = bigram_to_num(x1) - bigram_to_num(x2)
        a = solve_equation(x_diff, y_diff, m * m)
        if a != -1:
            b = (bigram_to_num(y1) - a * bigram_to_num(x1)) % (m * m)
            keys.append((a, b))
    return keys

def decrypt_with_keys(encrypted, keys):
    for a, b in keys:
        decrypted = decrypt_text(a, b, encrypted)
        if decrypted != -1:
            print(f"Ключ: a = {a}, b = {b}")
            print(f"Розшифрований текст: {decrypted}")


def main():
    encrypted_text = read_file('05_utf8.txt')
    open_bigrams = ['ст', 'но', 'ен', 'ни', 'от']
    encrypted_bigrams = ['вн', 'тн', 'дк', 'хщ', 'ун']
    keys = generate_keys(open_bigrams, encrypted_bigrams)
    decrypt_with_keys(encrypted_text, keys)

if __name__ == "__main__":
    main()
