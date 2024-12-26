import random
import math

#Алгоритм Евкліда
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#Ознака подільності Паскаля
def pascal_div(N, m, B=10):
    num_part = []
    while N > 0:
        num_part.append(N % B)
        N //= B

    r = [1]
    for i in range(1, len(num_part)):
        r.append((r[i - 1] * B) % m)

    excess = sum(d * r[i] for i, d in enumerate(num_part)) % m
    return excess == 0

#Тест на пробні ділення
def trial_div(N):
    small_prime = [2, 3, 5, 7, 11]
    for prime_num in small_prime:
        if pascal_div(N, prime_num):
            return False
    return True

#Тест Міллера-Рабіна
def mil_rab_test(p, k=10):
    if p < 2 or p % 2 == 0:
        return p == 2
    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    def check(x):
        x = pow(x, d, p)
        if x == 1 or x == p - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                return False
        return True

    counter = 0
    for _ in range(k):
        x = random.randint(2, p - 2)
        if gcd(x, p) != 1:
            return False
        if check(x):
            return False
        counter += 1
    if counter < k:
        return False
    return True

#Генерація простого числа у заданому діапазоні
def find_prime(st, fin):
    while True:
        num = random.randint(st, fin)
        if trial_div(num) and mil_rab_test(num):
            return num

#Генеруємо пари простих чисел p, q
def get_two(bit_leng=256):
    st = 2 ** (bit_leng - 1)
    fin = 2 ** bit_leng - 1

    p = find_prime(st, fin)
    q = find_prime(st, fin)
    p1 = find_prime(st, fin)
    q1 = find_prime(st, fin)

    while p * q > p1 * q1:
        p1 = find_prime(st, fin)
        q1 = find_prime(st, fin)

    return (p, q), (p1, q1)

#Розширений алгоритм Евкліда
def adv_eucl(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = adv_eucl(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

#Знаходження оберненого за модулем
def inverse(a, m):
    gcd, x, _ = adv_eucl(a, m)
    if gcd != 1:
        return None
    return x % m

# Функція Ойлера
def func_oil(p, q):
    return (p - 1) * (q - 1)

#Генерація ключів RSA
def keys_rsa(bit_leng=256):
    (p, q), _ = get_two(bit_leng=256)
    n = p * q
    phi = func_oil(p, q)
    e = 65537
    if gcd(e, phi) != 1:
        raise ValueError("Значення e має бути взаємнопростим із функцією Ойлера!")
    d = inverse(e, phi)
    return (d, p, q), (n, e)

#Шифрування повідомлення (викор. відкритий ключ)
def encrypt(M, public_key):
    n, e = public_key
    return pow(M, e, n)

#Розшифрування повідомлення (викор. секретний ключ)
def decrypt(cipher, secret_key):
    d, p, q = secret_key
    n = p * q
    return pow(cipher, d, n)

#Створює цифровий підпис
def digit_signature(M, secret_key):
    d, p, q = secret_key
    n = p * q
    return pow(M, d, n)

#Перевіряє цифровий підпис
def ver_signature(M, digit_signature, public_key):
    n, e = public_key
    return pow(digit_signature, e, n) == M

#Відправлення ключа
def k_send(k, send_secr_k, send_publ_k, rec_publ_k):
    key_encr = encrypt(k, rec_publ_k)
    key_signature = digit_signature(k, send_secr_k)
    encr_signature = encrypt(key_signature, rec_publ_k)
    return key_encr, encr_signature

#Отримання ключа
def k_receive(encr_secr_k, encr_signature, rec_secr_k, send_publ_k):
    key_decr = decrypt(encr_secr_k, rec_secr_k)
    decr_signature = decrypt(encr_signature, rec_secr_k)
    check_signature = ver_signature(key_decr, decr_signature, send_publ_k)
    return key_decr, check_signature

if __name__ == "__main__":
    st = int(input("Початок діапазону: "))
    fin = int(input("Кінець діапазону: "))

    print("Генерація простого числа...")
    prime_num = find_prime(st, fin)
    print(f"Просте число: {prime_num}")

    print("-----")
    print("Генерація пар ключів...")
    a_k = keys_rsa()
    b_k = keys_rsa()
    secr_a_k, publ_a_k = a_k
    secr_b_k, publ_b_k = b_k

    print(f"Абонент A: Секретний ключ: d = {secr_a_k[0]}, Відкритий ключ: n = {publ_a_k[0]}, e = {publ_a_k[1]}")
    print(f"Абонент B: Секретний ключ: d1 = {secr_b_k[0]}, Відкритий ключ: n1 = {publ_b_k[0]}, e1 = {publ_b_k[1]}")

    print("-----")
    print("Пари простих чисел p і q:")
    print(f"Абонент A: p = {secr_a_k[1]}, q = {secr_a_k[2]}")
    print(f"Абонент B: p1 = {secr_b_k[1]}, q1 = {secr_b_k[2]}")

    a_M = random.randint(1000, 9999)
    b_M = random.randint(1000, 9999)

    print("-----")
    print(f"Повідомлення від A до В: {a_M}")
    encr_a_M = encrypt(a_M, publ_a_k)
    print(f"Зашифроване: {encr_a_M}")

    decr_a_M = decrypt(encr_a_M, secr_b_k)
    print(f"Розшифроване: {decr_a_M}")

    print("-----")
    print(f"Повідомлення від B до A: {b_M}")
    encr_b_M = encrypt(b_M, publ_b_k)
    print(f"Зашифроване: {encr_b_M}")

    decr_b_M = decrypt(encr_b_M, secr_a_k)
    print(f"Розшифроване: {decr_b_M}")

    digital_s_a = digit_signature(a_M, secr_a_k)
    digital_s_b = digit_signature(b_M, secr_b_k)

    print("-----")
    print(f"Цифровий підпис від A: {digital_s_a}")
    print(f"Цифровий підпис від B: {digital_s_b}")

    print(f"Перевірка підпису A: {'Коректний' if ver_signature(a_M, digital_s_a, publ_a_k) else 'Некоректний'}")
    print(f"Перевірка підпису B: {'Коректний' if ver_signature(b_M, digital_s_b, publ_b_k) else 'Некоректний'}")

    k = random.randint(1, publ_b_k[1] - 1)
    key_encr, encr_signature = k_send(k, secr_a_k, publ_a_k, publ_b_k)
    print("-----")
    print(f"Переданий ключ від A до B: {k}")
    print(f"Зашифрований ключ: {key_encr}")
    print(f"Зашифрований підпис: {encr_signature}")

    key_decr, check_signature = k_receive(key_encr, encr_signature, secr_b_k, publ_a_k)
    print(f"Розшифрований ключ: {key_decr}")
    print(f"Підтвердження підпису: {'Вірний' if check_signature else 'Невірний'}")