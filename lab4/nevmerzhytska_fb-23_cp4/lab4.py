import random
from math import gcd

# Параметри
min_limit = 2 ** 256 - 1
max_limit = 2 ** 257
exponent = 2 ** 16 + 1  # Зазвичай 65537

# Алгоритм Миллера-Рабіна для перевірки простоти числа
def miller_rabin(n, k=5):
    """Перевірка на простоту за допомогою тесту Миллера-Рабіна."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Розкладаємо n-1 на 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Виконуємо k перевірок
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)  # x^2 % n
            if x == n - 1:
                break
        else:
            return False
    return True

# Функція перевірки простоти за допомогою алгоритму Миллера-Рабіна
def find_prime():
    while True:
        candidate_num = random.randint(min_limit, max_limit)
        print(f"Перевірка числа: {candidate_num}")
        if miller_rabin(candidate_num):
            print("Число є простим числом")
            return candidate_num
        else:
            print("Число не є простим числом")

# Розширений алгоритм Евкліда для обчислення оберненого елементу
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Створення ключів з використанням додаткової оптимізації
def create_keys(p, q):
    modulus = p * q  # Модуль для ключів
    totient = (p - 1) * (q - 1)  # Функція Ейлера

    # Вибір елемента, який є взаємно простим з totient
    exp = exponent
    while gcd(exp, totient) != 1:
        exp += 2

    # Знаходження секретного ключа
    _, private, _ = extended_gcd(exp, totient)
    private = private % totient  # Приведення до невід'ємного залишку

    return (modulus, exp), (private, p, q)

# Шифрування повідомлення з додатковою обробкою
def encrypt_message(plaintext, pub_key):
    modulus, exp = pub_key
    ciphertext = pow(plaintext, exp, modulus)
    return ciphertext

# Дешифрування повідомлення з додатковою обробкою
def decrypt_message(ciphertext, priv_key):
    private, p, q = priv_key
    modulus = p * q
    decrypted = pow(ciphertext, private, modulus)
    return decrypted

# Підписування повідомлення з додатковим етапом шифрування
def sign_message(message, priv_key):
    private, p, q = priv_key
    modulus = p * q
    signature = pow(message, private, modulus)
    return signature

# Перевірка підпису з додатковими перевірками
def verify_sign(message, signature, pub_key):
    modulus, exp = pub_key
    computed = pow(signature, exp, modulus)
    return message == computed

# Обмін ключами з додатковими перевірками
def exchange_key(key, sender_priv_key, receiver_pub_key):
    enc_key = encrypt_message(key, receiver_pub_key)
    sign = sign_message(key, sender_priv_key)
    enc_sign = encrypt_message(sign, receiver_pub_key)
    return enc_key, enc_sign

# Прийом ключів з додатковою перевіркою
def receive_exchange_key(enc_key, enc_sign, receiver_priv_key, sender_pub_key):
    key = decrypt_message(enc_key, receiver_priv_key)
    signature = decrypt_message(enc_sign, receiver_priv_key)
    if verify_sign(key, signature, sender_pub_key):
        return key
    return None

# Забезпечення правильного порядку p*q < p1*q1 з додатковими перевірками
def ensure_pq_less_than_p1q1():
    print(f"Генерація першого простого числа: {(p := find_prime())}")
    print(f"Генерація другого простого числа: {(q := find_prime())}")
    print(f"Генерація третього простого числа: {(p1 := find_prime())}")
    print(f"Генерація четвертого простого числа: {(q1 := find_prime())}")
    
    while (p * q) > (p1 * q1):
        print(f"pq = {p * q} > p1q1 = {p1 * q1}, перегенерація p1 і q1")
        print(f"Генерація нового p1: {(p1 := find_prime())}")
        print(f"Генерація нового q1: {(q1 := find_prime())}")
    
    return (p, q), (p1, q1)

# Основний процес з додатковими перевірками
def main_process():
    print("Генерація простих чисел для абонентів А і В:")
    (p, q), (p1, q1) = ensure_pq_less_than_p1q1()
    print(f"\nПара простих чисел для абонента А: p={p}, q={q}")
    print(f"\nПара простих чисел для абонента В: p={p1}, q={q1}")
    print(f"\nПеревірка: pq = {p * q} ≤ p1q1 = {p1 * q1}")

    print("\nГенерація ключів для абонентів А і В:")
    X_public_key, X_private_key = create_keys(p, q)
    Y_public_key, Y_private_key = create_keys(p1, q1)
    print(f"\nКлючі абонента А: {X_public_key}")
    print(f"Секретний ключ: {X_private_key}")
    print(f"\nКлючі абонента В: {Y_public_key}")
    print(f"Секретний ключ: {Y_private_key}\n")

    for ab in (("А", X_public_key, X_private_key), ("В", Y_public_key, Y_private_key)):
        print(f"Перевірка шифрування, розшифрування та підпису для абонента {ab[0]}")
        message = random.randint(0, ab[1][0] - 1)
        print(f"Повідомлення: {message}")
        encrypted_msg = encrypt_message(message, ab[1])
        print(f"Зашифроване повідомлення: {encrypted_msg}")
        decrypted_msg = decrypt_message(encrypted_msg, ab[2])
        print(f"Розшифроване повідомлення: {decrypted_msg}")
        if message == decrypted_msg:
            print("Повідомлення розшифровано правильно")
        else:
            print("Повідомлення розшифровано неправильно")
        signature = sign_message(message, ab[2])
        is_valid = verify_sign(message, signature, ab[1])
        print(f"Цифровий підпис: {signature}")
        if is_valid:
            print("Підпис дійсний")
        else:
            print("Підпис недійсний")
        print()

# Запуск
if __name__ == "__main__":
    main_process()
