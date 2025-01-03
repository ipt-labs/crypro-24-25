import random
from math import gcd

# перевірка простоти методом Міллера-Рабіна
def miller_r(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

   
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

# Функція для пошуку випадкового простого числа в заданому діапазоні
def gen_number(start, end):
    while True:
        num = random.randint(start, end)
        if miller_r(num):
            return num

# Функція для пошуку випадкового простого числа заданої довжини у бітах
def gen_bits(bit_length):
    while True:
        # Генеруємо випадкове число заданої довжини
        num = random.getrandbits(bit_length)
        num |= (1 << (bit_length - 1)) | 1  # Забезпечуємо старший і молодший біти = 1

        # Перевіряємо простоту
        if  miller_r(num):
            return num

# Функція для генерації двох пар простих чисел, що задовольняють умову pq <= p1q1
def gen_pairs(bit_length):
    while True:
        # Генерація випадкових простих чисел для пари A та пари B
        p = gen_bits(bit_length)
        q = gen_bits(bit_length)
        p1 = gen_bits(bit_length)
        q1 = gen_bits(bit_length)

        # Перевірка умови pq <= p1q1
        if p * q <= p1 * q1:
            return (p, q), (p1, q1)

# Генерація простого числа в діапазоні від 10 до 100
random_gen_number = gen_number(10, 100)

# Генерація пар простих чисел довжиною не менше 256 біт
bit_length = 256
(for_a, for_b) = gen_pairs(bit_length)

'''
print("Випадкове просте число в діапазоні:", random_gen_number)
print("Пара для абонента A:", for_a)
print("Пара для абонента B:", for_b)
'''
#################################

def GenerateKeyPair(bit_length):
    def mod_inverse(a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    p = gen_bits(bit_length)
    q = gen_bits(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = mod_inverse(e, phi)
    return (e, n), (d, p, q)

public_a, private_a = GenerateKeyPair(bit_length)      # Створення ключових пар
public_b, private_b = GenerateKeyPair(bit_length)

print("Відкритий ключ A:", public_a)
print("Секретний ключ A:", private_a)
print("Відкритий ключ B:", public_b)
print("Секретний ключ B:", private_b)

def Encrypt(M, public_key):
    e, n = public_key
    return pow(M, e, n)

def Decrypt(C, private_key):
    d, p, q = private_key
    n = p * q
    return pow(C, d, n)

def Sign(M, private_key):
    d, p, q = private_key
    n = p * q
    return pow(M, d, n)

def Verify(S, message, public_key):
    e, n = public_key
    return pow(S, e, n) == message

M = random.randint(10000000000, 99999999999)   # повідомлення

cipher_a = Encrypt(M, public_a)                # шифрування та розшифрування для A і В
decrypted_a = Decrypt(cipher_a, private_a)
cipher_b = Encrypt(M, public_b)
decrypted_b = Decrypt(cipher_b, private_b)

signature_a = Sign(M, private_a)               # створення та перевірка підписів для A і В
verified_a = Verify(signature_a, M, public_a)
signature_b = Sign(M, private_b)
verified_b = Verify(signature_b, M, public_b)

print("Повідомлення:", M)
print("Зашифроване повідомлення для A:", cipher_a)
print("Розшифроване повідомлення для A:", decrypted_a)
print("Зашифроване повідомлення для B:", cipher_b)
print("Розшифроване повідомлення для B:", decrypted_b)
print("Підпис для A:", signature_a)
print("Перевірка підпису A:", verified_a)
print("Підпис для B:", signature_b)
print("Перевірка підпису B:", verified_b)

'''
# Перевірка з тестовим середовищем:

M = int('d89122b77e', 16)
key = (int('10001', 16), int('9877D22722D834616FDD95CB4FEEEC9CCF36BD7163B46900BDF1AA7FFF1690F5', 16))
signature = int('83E2795046D06B0BF78BDF411C4D1F2065C7236CB5E77BDE3ADE7347C3E9D4DF', 16)
X = Encrypt(M, key)
Y = Verify(signature, M, key)
print(hex(X)[2:])
print(Y)
'''

def SendKey(k, public_b, private_a):
    e1, n1 = public_b
    d, p, q = private_a
    n = p * q


    k1 = pow(k, e1, n1)

    S1 = pow(k, d, n)

    return k1, S1

def ReceiveKey(k1, S1, private_b, public_a):
    d, p, q = private_b
    n1 = p * q
    e, n = public_a

    k = pow(k1, d, n1)

    S = pow(S1, e, n)

    is_valid = (k == S)                
    return k, is_valid


k = random.randint(1, public_a[1] - 1)  # 0 < k < n
print(f"Секретний ключ k: {k}")

# Відправка ключа від A до B
k1, S1 = SendKey(k, public_b, private_a)
print(f"Відправлені дані: k1 = {k1}, S1 = {S1}")

# Отримання ключа на боці B
received_k, is_valid = ReceiveKey(k1, S1, private_b, public_a)
print(f"Отриманий ключ: {received_k}")
print(f"Перевірка автентичності: {'Успішно' if is_valid else 'Неуспішно'}")

# Перевірка коректності передачі
assert k == received_k, "Помилка передачі ключа!"

