
import random
from math import gcd

#-------------------------option 1-------------------------

# Перевірка на простоту методом пробних ділень
def is_prime_trial_division(n):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0 and n != p:
            return False
    return True

# Імовірнісний тест Міллера-Рабіна
def miller_rabin_test(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Представлення n-1 у вигляді 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    def check_composite(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        if check_composite(a):
            return False
    return True

# Генерація випадкового простого числа заданої довжини в бітах
def generate_random_prime(bit_length):
    while True:
        candidate = random.getrandbits(bit_length) | (1 << (bit_length - 1)) | 1
        if is_prime_trial_division(candidate) and miller_rabin_test(candidate):
            return candidate

#-------------------------option 2-------------------------

# Генерація двох пар простих чисел (p, q) та (p1, q1), де pq <= p1q1
def generate_prime_pairs(bit_length):
    # Генерація першої пари для абонента A
    p = generate_random_prime(bit_length)
    q = generate_random_prime(bit_length)
    
    # Генерація другої пари для абонента B
    p1 = generate_random_prime(bit_length)
    q1 = generate_random_prime(bit_length)
    # # Перевірка умови pq <= p1q1
    if p*q <= p1*q1:
        return (p, q), (p1, q1)
    return (p1, q1), (p, q)

#-------------------------option 3-------------------------

# Генерує секретний та відкритий ключі для RSA
def generate_rsa_keypair(p, q):

    # Обчислення n та функції Ейлера φ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Генерація відкритої експоненти e (взаємно простої з φ(n))
    e = 65537  # Стандартний вибір для RSA
    if gcd(e, phi_n) != 1:
        # Якщо e не взаємно просте з φ(n), вибираємо інше
        while True:
            e = random.randint(2, phi_n - 1)
            if gcd(e, phi_n) == 1:
                break

    # Обчислення секретного ключа d (обернений за модулем φ(n))
    d = pow(e, -1, phi_n)

    # Повернення секретного (d, p, q) та відкритого (e, n) ключів
    return (d, p, q), (e, n)

# Побудова схем RSA для абонентів A та B
def rsa_setup(p, q, p1, q1):
    # Генерація ключових пар для абонента A
    private_key_a, public_key_a = generate_rsa_keypair(p, q)

    # Генерація ключових пар для абонента B
    private_key_b, public_key_b = generate_rsa_keypair(p1, q1)

    return private_key_a, public_key_a, private_key_b, public_key_b

#-------------------------option 4-------------------------

# Функція шифрування повідомлення.
def encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)

# Функція розшифрування повідомлення
def decrypt(ciphertext, private_key):
    d, p, q = private_key
    n = p * q
    return pow(ciphertext, d, n)

# Функція створення цифрового підпису
def sign(message, private_key):
    d, p, q = private_key
    n = p * q
    return pow(message, d, n)

# Функція перевірки цифрового підпису
def verify(message, signature, public_key):
    e, n = public_key
    return pow(signature, e, n) == message

#-------------------------option 5-------------------------

def send_key(k, sender_private_key, sender_public_key, recipient_public_key):
    """
    Функція відправника (абонента A), яка формує зашифроване повідомлення з підписом.
    k - секретний ключ, який потрібно передати
    sender_private_key - приватний ключ відправника
    sender_public_key - публічний ключ відправника
    recipient_public_key - публічний ключ одержувача
    """
    # Шифрування ключа k для отримувача
    encrypted_key = encrypt(k, recipient_public_key)
    
    # Створення цифрового підпису для k
    signature = sign(k, sender_private_key)
    
    # Зашифрування підпису для отримувача
    encrypted_signature = encrypt(signature, recipient_public_key)
    
    # Повертається зашифрований ключ та підпис
    return encrypted_key, encrypted_signature

def receive_key(encrypted_key, encrypted_signature, recipient_private_key, sender_public_key):
    """
    Функція отримувача (абонента B), яка приймає зашифроване повідомлення та перевіряє підпис.
    encrypted_key - зашифрований ключ k
    encrypted_signature - зашифрований підпис
    recipient_private_key - приватний ключ отримувача
    sender_public_key - публічний ключ відправника
    """
    # Розшифрування ключа k
    decrypted_key = decrypt(encrypted_key, recipient_private_key)
    
    # Розшифрування підпису
    decrypted_signature = decrypt(encrypted_signature, recipient_private_key)
    
    # Перевірка підпису
    is_valid_signature = verify(decrypted_key, decrypted_signature, sender_public_key)
    
    return decrypted_key, is_valid_signature

#---------------------------------------------------------------------

def main(bit_length=256):
    random_prime = generate_random_prime(bit_length)
    print("\n")
    print("-"*100)
    print(f"Випадкове просте число ({bit_length} біт): {random_prime}\n")

# ---------------------------------------------------------------------
    pair_A, pair_B = generate_prime_pairs(bit_length) # this function returns (p, q), (p1, q1) if pq < p1q1
    print("-"*100)
    print(f"Пара для абонента A:\n\tp = {pair_A[0]},\n\tq = {pair_A[1]}\n")
    print(f"Пара для абонента B: \n\tp1 = {pair_B[0]}, \n\tq1 = {pair_B[1]}\n")

#----------------------------------------------------------------------
    private_a, public_a, private_b, public_b = rsa_setup(pair_A[0], pair_A[1], pair_B[0], pair_B[1])
    print("-"*100)
    print(f"Відкритий ключ A:\n\te = {public_a[0]},\n\tn = {public_a[1]}\n")
    print(f"Секретний ключ A:\n\td = {private_a[0]},\n\tp = {private_a[1]},\n\tq = {private_a[2]}\n")
    print(f"Відкритий ключ B:\n\te = {public_b[0]},\n\tn = {public_b[1]}\n")
    print(f"Секретний ключ B:\n\td = {private_b[0]},\n\tp = {private_b[1]},\n\tq = {private_b[2]}\n")

#----------------------------------------------------------------------
    # Повідомлення для шифрування та підпису
    message = 37462138794623786428372

    # Абонент A шифрує повідомлення для B
    ciphertext = encrypt(message, public_b)
    print("-"*100)
    print(f"Повідомлення для шифрування та підпису: {message}\n")
    print(f"Зашифроване повідомлення: {ciphertext}\n")

    # Абонент B розшифровує повідомлення
    decrypted_message = decrypt(ciphertext, private_b)
    print(f"Розшифроване повідомлення: {decrypted_message}\n")

    # Абонент A створює цифровий підпис для повідомлення
    signature = sign(message, private_a)
    print(f"Цифровий підпис: {signature}\n")

    # Абонент B перевіряє цифровий підпис
    is_valid = verify(message, signature, public_a)
    print(f"Цифровий підпис вірний: {is_valid}\n")

#-----------------------------------------------------------------------
    # Випадковий ключ k для передачі
    k = random.randint(1, public_b[1] - 1)

    print("-"*100)
    print(f"Секретний ключ для передачі: {k}\n")

    # Відправник A формує повідомлення
    encrypted_key, encrypted_signature = send_key(k, private_a, public_a, public_b)

    print(f"Зашифрований ключ: {encrypted_key}\n")
    print(f"Зашифрований підпис: {encrypted_signature}\n")

    # Одержувач B приймає повідомлення
    decrypted_key, is_valid_signature = receive_key(encrypted_key, encrypted_signature, private_b, public_a)

    print(f"Розшифрований ключ: {decrypted_key}\n")
    print(f"Підпис коректний: {is_valid_signature}")
    print("-"*100)

if __name__ == "__main__":
    bit_length=256
    main(bit_length)