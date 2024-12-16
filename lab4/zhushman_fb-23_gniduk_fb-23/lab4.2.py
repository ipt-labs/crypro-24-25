import random
from math import gcd

def mod_inverse(e, phi):
    """Обчислює мультиплікативний обернений для e за модулем phi."""
    a, b, x0, x1 = phi, e, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
    return x0 % phi

def is_prime_miller_rabin(n, k=5):
    """Перевірка числа n на простоту тестом Міллера-Рабіна."""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
        if n == p:
            return True
        if n % p == 0:
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

def generate_prime_in_bit_range(min_bits, max_bits):
    """
    Генерує випадкове просте число у діапазоні бітів [min_bits, max_bits].
    """
    if min_bits < 2 or max_bits < min_bits:
        raise ValueError("Некоректний діапазон бітів.")
    
    while True:
        lower_bound = 1 << (min_bits - 1)  
        upper_bound = (1 << max_bits) - 1
        candidate = random.randint(lower_bound, upper_bound)
        candidate |= 1
        if is_prime_miller_rabin(candidate):
            return candidate

def generateKeyPair(bits=256):
    """Генерує пару ключів RSA: відкритий (e, n) та секретний (d, p, q)."""
    p = generate_prime_in_bit_range(bits, bits)
    q = generate_prime_in_bit_range(bits, bits)
    while p == q: 
        q = generate_prime_in_bit_range(bits, bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537 
    if gcd(e, phi) != 1:
        e = random.randrange(2, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    
    return (e, n), (d, p, q)

def encrypt(message, e, n):
    """Шифрує повідомлення для відкритого ключа (e, n)."""
    return pow(message, e, n)

def decrypt(ciphertext, d, n):
    """Розшифровує повідомлення за секретним ключем (d, n)."""
    return pow(ciphertext, d, n)

def sign(message, d, n):
    """Створює цифровий підпис повідомлення."""
    return pow(message, d, n)

def verify(signature, e, n, original_message):
    """Перевіряє цифровий підпис."""
    return pow(signature, e, n) == original_message

def generate_random_message(n):
    """Генерує випадкове повідомлення M, яке менше за n."""
    return random.randint(1, n - 1)

def sendkey(key, sender_private_key, sender_public_key, receiver_public_key):
    """
    Протокол відправника: шифрує ключ для отримувача і створює цифровий підпис.
    """
    # Шифрування ключа відкритим ключем отримувача
    encrypted_key = encrypt(key, receiver_public_key[0], receiver_public_key[1])

    # Підписання ключа секретним ключем відправника
    signature = sign(key, sender_private_key[0], sender_public_key[1])
    
    return encrypted_key, signature

def receivekey(encrypted_key, signature, sender_public_key, receiver_private_key, receiver_public_key):
    """
    Протокол отримувача: розшифровує ключ і перевіряє цифровий підпис відправника.
    """
    # Розшифрування ключа за допомогою секретного ключа отримувача
    decrypted_key = decrypt(encrypted_key, receiver_private_key[0], receiver_public_key[1])
    
    # Перевірка цифрового підпису відправника
    is_valid = verify(signature, sender_public_key[0], sender_public_key[1], decrypted_key)
    
    return decrypted_key, is_valid

keypair_A = generateKeyPair()
keypair_B = generateKeyPair()

(e_A, n_A), (d_A, p_A, q_A) = keypair_A
(e_B, n_B), (d_B, p_B, q_B) = keypair_B

print("Ключі для абонента A:")
print(f"Відкритий ключ: (e = {e_A}, n = {n_A})")
print(f"Секретний ключ: (d = {d_A}, p = {p_A}, q = {q_A})")

print("\nКлючі для абонента B:")
print(f"Відкритий ключ: (e = {e_B}, n = {n_B})")
print(f"Секретний ключ: (d = {d_B}, p = {p_B}, q = {q_B})")

# 1 Шифрування та розшифрування для абонента A
message_A = generate_random_message(n_A)
print(f"\nВідкрите повідомлення для A: {message_A}")

ciphertext_A = encrypt(message_A, e_A, n_A)
print(f"Криптограма для A: {ciphertext_A}")

decrypted_message_A = decrypt(ciphertext_A, d_A, n_A)
print(f"Розшифроване повідомлення для A: {decrypted_message_A}")

# Перевіряємо правильність розшифрування
assert message_A == decrypted_message_A, "Розшифрування для A некоректне!"

# 2 Шифрування та розшифрування для абонента B
message_B = generate_random_message(n_B)
print(f"\nВідкрите повідомлення для B: {message_B}")

ciphertext_B = encrypt(message_B, e_B, n_B)
print(f"Криптограма для B: {ciphertext_B}")

decrypted_message_B = decrypt(ciphertext_B, d_B, n_B)
print(f"Розшифроване повідомлення для B: {decrypted_message_B}")

# Перевіряємо правильність розшифрування
assert message_B == decrypted_message_B, "Розшифрування для B некоректне!"

# 3 Створення та перевірка цифрового підпису для A
signature_A = sign(message_A, d_A, n_A)
print(f"\nЦифровий підпис повідомлення для A: {signature_A}")

is_valid_signature_A = verify(signature_A, e_A, n_A, message_A)
print(f"Перевірка підпису для A: {'Валідний' if is_valid_signature_A else 'Невалідний'}")

# 4 Створення та перевірка цифрового підпису для B
signature_B = sign(message_B, d_B, n_B)
print(f"\nЦифровий підпис повідомлення для B: {signature_B}")

is_valid_signature_B = verify(signature_B, e_B, n_B, message_B)
print(f"Перевірка підпису для B: {'Валідний' if is_valid_signature_B else 'Невалідний'}")

"""----"""
# Генеруємо ключову пару для A і B
public_A, private_A = generateKeyPair()
public_B, private_B = generateKeyPair()

# Випадковий ключ k, 0 < k < n_B
key_k = generate_random_message(public_B[1])
print(f"\nВипадковий ключ k: {key_k}")

# Відправник A шифрує ключ для B і підписує його
encrypted_key, signature = sendkey(key_k, private_A, public_A, public_B)
print(f"\nВідправник A:")
print(f"Зашифрований ключ: {encrypted_key}")
print(f"Цифровий підпис: {signature}")

# Отримувач B розшифровує ключ і перевіряє підпис
decrypted_key, is_valid_signature = receivekey(encrypted_key, signature, public_A, private_B, public_B)

print(f"\nОтримувач B:")
print(f"Розшифрований ключ: {decrypted_key}")
print(f"Перевірка підпису: {'Валідний' if is_valid_signature else 'Невалідний'}")

# Перевірка коректності розшифрування
assert key_k == decrypted_key, "Розшифрований ключ не збігається з вихідним!"
print("\nПередача ключа від A до B завершена")
