import random
from math import gcd


def is_prime(p, primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], k=10):
    for prime in primes:
        if p % prime == 0:
            return False

    s, d = 0, p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        x = random.randrange(2, p)
        y = pow(x, d, p)

        if gcd(x, p) != 1:
            return False

        if y in (1, p - 1):
            continue

        for _ in range(s - 1):
            y = pow(y, 2, p)
            if y == 1:
                return False
            elif y == p - 1:
                break
        else:
            return False
    return True


def GeneratePrime(bits):
    while True:
        x = random.getrandbits(bits) | (1 << (bits - 1)) | 1

        if is_prime(x):
            return x
        else:
            print(f"Кандидат {x} не є простим числом")


def GenerateKeyPair(p, q):
    n = p * q
    f = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, f)
    return ((n, e), (d, p, q))


def Encrypt(message, public_key):
    n, e = public_key
    return pow(message, e, n)


def Decrypt(ciphertext, private_key):
    d, p, q = private_key
    n = p * q
    return pow(ciphertext, d, n)


def Sign(message, private_key):
    d, p, q = private_key
    n = p * q
    return pow(message, d, n)


def Verify(message, signature, public_key):
    n, e = public_key
    return pow(signature, e, n) == message


def SendKey(key, sender_private_key, receiver_public_key):
    k1 = Encrypt(key, receiver_public_key)
    signature = Sign(key, sender_private_key)
    signature1 = Encrypt(signature, receiver_public_key)
    return k1, signature1


def ReceiveKey(encrypted_key, encrypted_signature, receiver_private_key, sender_public_key):
    k = Decrypt(encrypted_key, receiver_private_key)
    signature = Decrypt(encrypted_signature, receiver_private_key)
    if Verify(k, signature, sender_public_key):
        return k
    return None


def main():
    print("Генерація простих чисел для абонентів А і В")
    bits = 256

    while True:
        p = GeneratePrime(bits)
        q = GeneratePrime(bits)
        p1 = GeneratePrime(bits)
        q1 = GeneratePrime(bits)
        print(f"Перевірка потенційних пар простих чисел: p={p}, q={q}, p1={p1}, q1={q1}")

        if p * q <= p1 * q1:
            break

    print(f"Пара простих чисел для абонента А: p={p}, q={q}")
    print(f"Пара простих чисел для абонента В: p={p1}, q={q1}")
    print()

    print("Генерація ключів для абонентів А і В")
    A_public_key, A_private_key = GenerateKeyPair(p, q)
    B_public_key, B_private_key = GenerateKeyPair(p1, q1)
    print("Ключі абонента А:")
    print(f"Відкритий ключ (n, e): {A_public_key}")
    print(f"Секретний ключ (d, p, q): {A_private_key}")
    print()
    print("Ключі абонента В:")
    print(f"Відкритий ключ (n, e): {B_public_key}")
    print(f"Секретний ключ (d, p, q): {B_private_key}")
    print()

    for x in (("А", A_public_key, A_private_key), ("В", B_public_key, B_private_key)):
        print(f"Перевірка шифрування, розшифрування та підпису для абонента {x[0]}")
        message = random.randint(0, x[1][0] - 1)
        print(f"Повідомлення: {message}")
        encrypted_message = Encrypt(message, x[1])
        print(f"Зашифроване повідомлення: {encrypted_message}")
        decrypted_message = Decrypt(encrypted_message, x[2])
        print(f"Розшифроване повідомлення: {decrypted_message}")
        if message == decrypted_message:
            print("Повідомлення розшифровано правильно")
        else:
            print("Повідомлення розшифровано неправильно")
        signature = Sign(message, x[2])
        print(f"Цифровий підпис: {signature}")
        is_valid = Verify(message, signature, x[1])
        if is_valid:
            print("Підпис дійсний")
        else:
            print("Підпис недійсний")
        print()

    print("Перевірка протоколу розсилання ключів")
    key = random.randint(1, A_public_key[0] - 1)
    print(f"Ключ: {key}")
    encrypted_key, encrypted_signature = SendKey(key, A_private_key, B_public_key)
    print(f"Зашифрований ключ: {encrypted_key}")
    print(f"Зашифрований підпис: {encrypted_signature}")
    received_key = ReceiveKey(encrypted_key, encrypted_signature, B_private_key, A_public_key)
    print(f"Отриманий ключ: {received_key}")
    if key == received_key:
        print("Ключ передано успішно")
    else:
        print("Помилка передачі ключа")


if __name__ == "__main__":
    main()
