import hashlib
import random
from math import gcd


# Завдання 1: Перевірка числа на простоту
def is_probable_prime(n, iterations=5):
    """Перевіряємо, чи є число n імовірно простим за допомогою тесту Міллера-Рабіна."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False


    # Розкладання n-1 у вигляді 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2


    # Локальна функція перевірки свідків складеності
    def is_composite(base):
        result = pow(base, d, n)
        if result in (1, n - 1):
            return False
        for _ in range(s - 1):
            result = pow(result, 2, n)
            if result == n - 1:
                return False
        return True


    for _ in range(iterations):
        candidate = random.randint(2, n - 2)
        if is_composite(candidate):
            return False
    return True


def find_prime(bit_size):
    """Генеруємо випадкове просте число заданого розміру в бітах."""
    while True:
        num = random.getrandbits(bit_size) | (1 << (bit_size - 1)) | 1
        if is_probable_prime(num):
            return num




# Завдання 2: Генерація пар простих чисел
def generate_key_pairs(size=256):
    """Створюємо дві пари простих чисел (p, q) і (p1, q1), дотримуючись умови p*q <= p1*q1."""
    while True:
        p, q = find_prime(size), find_prime(size)
        p1, q1 = find_prime(size), find_prime(size)
        if p * q <= p1 * q1:
            return (p, q), (p1, q1)




# Завдання 3: Генерація ключів RSA
def rsa_key_generation(prime1, prime2):
    """Генеруємо публічний та приватний ключі RSA на основі двох простих чисел."""
    modulus = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)


    # Пошук відкритої експоненти e
    public_exponent = 65537  # Стандартне значення
    if gcd(public_exponent, phi) != 1:
        for candidate in range(3, phi, 2):
            if gcd(candidate, phi) == 1:
                public_exponent = candidate
                break


    # Обчислення секретної експоненти d
    private_exponent = pow(public_exponent, -1, phi)


    # Повернення пари ключів
    return (public_exponent, modulus), (private_exponent, prime1, prime2)





# Функція для перетворення рядка в число
def string_to_number(message):
    return int.from_bytes(message.encode('utf-8'), 'big')

# Функція для перетворення числа в рядок
def number_to_string(number):
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, 'big').decode('utf-8', errors='ignore')

# Функція шифрування
def encrypt(message, public_key):
    e, n = public_key
    m = string_to_number(message)
    cipher = pow(m, e, n)
    return cipher

# Функція дешифрування
def decrypt(cipher, private_key):
    d, p, q = private_key
    n = p * q
    decrypted = pow(cipher, d, n)
    return number_to_string(decrypted)

# Функція хешування повідомлення (SHA-256)
def hash_message(message):
    return int(hashlib.sha256(message.encode('utf-8')).hexdigest(), 16)

# Функція підпису повідомлення
def sign_message(message, private_key):
    d, p, q = private_key
    n = p * q
    message_hash = hash_message(message)
    signature = pow(message_hash, d, n)
    return signature

# Функція перевірки підпису
def verify_signature(message, signature, public_key):
    e, n = public_key
    message_hash = hash_message(message)
    verified_hash = pow(signature, e, n)
    return message_hash == verified_hash

if __name__ == "__main__":
    message = "Hello, RSA!"
    print(f"\n Повідомлення для шифрування: {message}")

    # Приклад шифрування та дешифрування
    print('Розшифрувати повідомлення з сервера')
    
    public_key_a = (
        65537, 
        6178263559633057148267807723786822689853507354271103554805737053903986071238208067502946203776131463132298348011108982858765071921031193101260286905417517
        )
    
    private_key_a = (
        1208370573986855158559237673428742439210556743016113117254374438209580747686487537184350425347702431387234863951015319288419174432654233652304400063766457, 
        82401489338079545932457810672827645719787070425033484991970341676096304784619, 
        74977571513115179459869276594214486337005102965765164634907665882094565443143
        )
    
    encrypted_message = 3943341437669028212230546245688015304020085812894358406729217090350170765294999141260704744258064127544053973186585184940320148081729006037045501390745259
    
    decrypted_message = decrypt(encrypted_message, private_key_a)
    print(f"Дешифроване повідомлення: {decrypted_message}")

     # Приклад підпису та перевірки підпису
    signature = sign_message(message, private_key_a)
    print(f"Підпис повідомлення: {signature}")
    is_valid = verify_signature(decrypted_message, signature, public_key_a)
    print(f"Перевірка підпису: {'Дійсний' if is_valid else 'Недійсний'}")