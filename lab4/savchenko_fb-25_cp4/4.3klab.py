import random
from math import gcd



def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_val, x, y


def miller_rabin(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

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

def generate_r_prime(bit_length):
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1
        if miller_rabin(candidate):
            return candidate


def GenerateKeyPair(bit_length=256):
    p = generate_r_prime(bit_length)
    q = generate_r_prime(bit_length)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    while True:
        e = random.randint(217, phi_n - 1)
        if gcd(e, phi_n) == 1:
            break

    _, d, _ = extended_gcd(e, phi_n)
    d = d % phi_n
    if d < 0:
        d += phi_n

    public_key = (e, n)
    private_key = (d, p, q)
    return public_key, private_key

def Encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)

def Decrypt(ciphertext, private_key):
    d, p, q = private_key
    n = p * q
    return pow(ciphertext, d, n)


def Sign(message, private_key):
    d, p, q = private_key
    n = p * q
    return pow(message, d, n)

def Verify(signature, message, public_key):
    e, n = public_key
    return pow(signature, e, n) == message


def SendKey(key, sender_private_key, receiver_public_key):
    encrypted_key = Encrypt(key, receiver_public_key)
    signature = Sign(key, sender_private_key)
    return encrypted_key, signature

def ReceiveKey(encrypted_key, signature, sender_public_key, receiver_private_key):
    key = Decrypt(encrypted_key, receiver_private_key)
    is_valid = Verify(signature, key, sender_public_key)
    return key, is_valid



public_key_a, private_key_a = GenerateKeyPair(256)
public_key_b, private_key_b = GenerateKeyPair(256)


message = random.randint(1, public_key_a[1] - 1)
ciphertext = Encrypt(message, public_key_a)
decrypted_message = Decrypt(ciphertext, private_key_a)

print("Оригінальне повідомлення:", message)
print("Шифротекст:", ciphertext)
print("Розшифроване повідомлення:", decrypted_message)
assert message == decrypted_message, "Розшифрування некоректне!"


signature = Sign(message, private_key_a)
is_valid = Verify(signature, message, public_key_a)

print("\nЦифровий підпис:", signature)
print("Перевірка підпису:", is_valid)
assert is_valid, "Підпис некоректний!"


key_to_send = random.randint(1, public_key_b[1] - 1)
encrypted_key, signature = SendKey(key_to_send, private_key_a, public_key_b)
received_key, is_valid = ReceiveKey(encrypted_key, signature, public_key_a, private_key_b)

print("\nВідправлений ключ:", key_to_send)
print("Отриманий ключ:", received_key)
print("Перевірка ключа:", is_valid)
assert key_to_send == received_key and is_valid, "Протокол розсилання ключів некоректний!"

def ManualInput():
    # Виведення публічного ключа для користувача
    public_key = int(input('Public key: '), 16)
    e = int(input('Exponent: '), 16)

    # Повертаємо експоненту та модуль у вигляді кортежу
    return (e, public_key)

# Функція для шифрування
def Encrypt(message, public_key_a):
    e, n = public_key_a  
    #  стандарт RSA-алгоритм: c = m^e mod n
    return pow(message, e, n)



public_key_a = ManualInput()

message = int(input("Введіть повідомлення для шифрування: "), 16)
ciphertext = Encrypt(message, public_key_a)


formatted_ciphertext = hex(ciphertext)[2:].upper()
print("Шифротекст:", formatted_ciphertext)




