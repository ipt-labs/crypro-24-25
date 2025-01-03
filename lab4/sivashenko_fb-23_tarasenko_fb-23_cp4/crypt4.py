import random

class User:
    def __init__(self, name, public_key, private_key, certificate, certificate_verified):
        self.name = name
        self.public_key = public_key
        self.private_key = private_key
        self.certificate = certificate
        self.certificate_verified = certificate_verified

    def send_key(self, receiver, key):
        print(f"{self.name} надсилає ключ {receiver.name}.")
        encrypted_key = encrypt(key, receiver.public_key)  # Шифруємо ключ публічним ключем отримувача
        signature = sign(key, self.private_key)  # Створюємо цифровий підпис
        return encrypted_key, signature

    def receive_key(self, sender, encrypted_key, signature):
        print(f"{self.name} отримує ключ від {sender.name}.")
        key = decrypt(encrypted_key, self.private_key)  # Розшифровуємо ключ
        is_valid = verify(signature, key, sender.public_key)  # Перевіряємо підпис
        return key, is_valid


# Тест Міллера-Рабіна для перевірки на простоту
def is_prime(n, k=10):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Пробне ділення для невеликих простих чисел
    for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0 and n != p:
            return False

    # Представляємо n-1 як 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Виконуємо k ітерацій тесту Міллера-Рабіна
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Генерація випадкового простого числа заданої довжини
def generate_prime(bit_length):
    while True:
        candidate = random.getrandbits(bit_length) | (1 << (bit_length - 1)) | 1  
        if is_prime(candidate):
            return candidate

def generate_prime_pairs(bit_length):
    # Генерація чисел p, q для A
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)

    # Генерація чисел p1, q1 для B
    while True:
        p1 = generate_prime(bit_length)
        q1 = generate_prime(bit_length)
        if p * q <= p1 * q1:
            break

    return (p, q), (p1, q1)

from math import gcd

# Генерація ключів RSA
def generate_rsa_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Генерація e
    e = 65537  # Зазвичай використовується як стандартне значення
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Обчислення d (обернене до e по модулю phi)
    d = pow(e, -1, phi)

    # Повернення ключів
    return (n, e), (d, p, q)

def generate_rsa_schemes(bit_length=256):
    # Генерація пар простих чисел
    (p, q), (p1, q1) = generate_prime_pairs(bit_length)

    # Ключі для абонента A
    public_key_A, private_key_A = generate_rsa_keys(p, q)

    # Ключі для абонента B
    public_key_B, private_key_B = generate_rsa_keys(p1, q1)

    return {
        "A": {"public_key": public_key_A, "private_key": private_key_A},
        "B": {"public_key": public_key_B, "private_key": private_key_B}
    }


def encrypt(message, public_key):
    n, e = public_key
    assert message < n, "Повідомлення перевищує модуль n, шифрування неможливе!"
    return pow(message, e, n)

# Розшифрування повідомлення
def decrypt(ciphertext, private_key):
    d, p, q = private_key
    n = p * q
    return pow(ciphertext, d, n)

# Створення цифрового підпису
def sign(message, private_key):
    d, p, q = private_key
    n = p * q
    return pow(message, d, n)

# Перевірка цифрового підпису
def verify(signature, message, public_key):
    n, e = public_key
    return pow(signature, e, n) == message

# Вибір випадкового відкритого повідомлення M
def generate_message(bit_length):
    return random.getrandbits(bit_length - 1)  # Менше за n



def send_key(sender_private_key, receiver_public_key, K):
    # Шифруємо ключ K публічним ключем отримувача
    encrypted_key = encrypt(K, receiver_public_key)
    # Створюємо цифровий підпис для K
    signature = sign(K, sender_private_key)
    return encrypted_key, signature

# Протокол прийому ключа
def receive_key(sender_public_key, receiver_private_key, encrypted_key, signature):
    # Розшифровуємо ключ K
    K = decrypt(encrypted_key, receiver_private_key)
    # Перевіряємо підпис
    is_valid = verify(signature, K, sender_public_key)
    return K, is_valid

# Виконання протоколу
if __name__ == "__main__":
    rsa_keys = {
        "A": generate_rsa_keys(generate_prime(256), generate_prime(256)),
        "B": generate_rsa_keys(generate_prime(256), generate_prime(256)),
    }

    user_A = User("User A", rsa_keys["A"][0], rsa_keys["A"][1], None, True)
    user_B = User("User B", rsa_keys["B"][0], rsa_keys["B"][1], None, True)

    # Генерація відкритих повідомлень
    M1 = generate_message(256)
    M2 = generate_message(256)

    print(f"\nВідкрите повідомлення M1: {M1}")
    print(f"Відкрите повідомлення M2: {M2}\n")

    # Обмін зашифрованими повідомленнями через методи класу
    encrypted_M1, signature_A = user_A.send_key(user_B, M1)
    decrypted_M1, valid_signature_A = user_B.receive_key(user_A, encrypted_M1, signature_A)

    encrypted_M2, signature_B = user_B.send_key(user_A, M2)
    decrypted_M2, valid_signature_B = user_A.receive_key(user_B, encrypted_M2, signature_B)

    # Перевірка результатів
    print(f"\nРозшифроване M1 для B: {decrypted_M1}, підпис {'валідний' if valid_signature_A else 'невалідний'}")
    print(f"Розшифроване M2 для A: {decrypted_M2}, підпис {'валідний' if valid_signature_B else 'невалідний'}")
    assert M1 == decrypted_M1, "Розшифрування M1 некоректне!"
    assert M2 == decrypted_M2, "Розшифрування M2 некоректне!"

    print("\nКлючі користувачів:")
    print(f"User A:\n  Публічний ключ: {rsa_keys['A'][0]}\n  Приватний ключ: {rsa_keys['A'][1]}")
    print(f"\nUser B:\n  Публічний ключ: {rsa_keys['B'][0]}\n  Приватний ключ: {rsa_keys['B'][1]}")

    print("\nПротокол успішно завершено!")


