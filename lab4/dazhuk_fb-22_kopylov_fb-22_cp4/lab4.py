from rsa_helpers import *


def GenerateKeyPair(bits=256):
    """
    Генерація ключових пар для RSA.
    :param bits: Довжина простих чисел (в бітах).
    :return: Кортеж ((n, e), (d, p, q)), де
             (n, e) — відкритий ключ,
             (d, p, q) — секретний ключ.
    """
    # Крок 1: Генерація простих чисел p і q
    p, q = generate_prime_pair(bits)

    # Крок 2: Обчислення n = p * q і φ(n) = (p-1) * (q-1)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Крок 3: Вибір e (взаємно простого з φ(n))
    e = 65537

    # Крок 4: Обчислення d, оберненого до e за модулем φ(n)
    d = mod_inverse(e, phi_n)

    # Повернення відкритого і секретного ключів
    return (n, e), (d, p, q)


def Encrypt(message, public_key):
    """Шифрування повідомлення з використанням відкритого ключа."""
    n, e = public_key
    return modular_pow(message, e, n)


def Decrypt(ciphertext, private_key):
    """Розшифрування повідомлення з використанням секретного ключа."""
    d, p, q = private_key
    n = p * q
    return modular_pow(ciphertext, d, n)


def Sign(message, private_key):
    """Створення цифрового підпису для повідомлення."""
    d, p, q = private_key
    n = p * q
    return modular_pow(message, d, n)


def Verify(signature, message, pub_key):
    """Перевірка цифрового підпису."""
    n, e = pub_key
    return message == modular_pow(signature, e, n)


def SendKey(public_key_receiver, private_key_sender, k):
    """
    Відправлення зашифрованого ключа з цифровим підписом.
    :param public_key_receiver: Відкритий ключ отримувача.
    :param private_key_sender: Секретний ключ відправника.
    :param k: Повідомлення (ключ), що передається.
    :return: Кортеж (зашифрований ключ, зашифрований цифровий підпис).
    """
    encrypted_key = Encrypt(k, public_key_receiver)

    key_signature = Sign(k, private_key_sender)

    encrypted_key_signature = Encrypt(key_signature, public_key_receiver)

    return encrypted_key, encrypted_key_signature


def ReceiveKey(encrypted_key, encrypted_key_signature, public_key_sender, private_key_receiver):
    """
    Прийом зашифрованого ключа та перевірка його автентичності.
    :param encrypted_key: Зашифроване повідомлення (ключ).
    :param encrypted_key_signature: Зашифрований цифровий підпис відправника.
    :param public_key_sender: Відкритий ключ відправника.
    :param private_key_receiver: Секретний ключ отримувача.
    :return: Розшифроване повідомлення (ключ) та результат перевірки.
    """
    decrypted_key = Decrypt(encrypted_key, private_key_receiver)

    decrypted_key_signature = Decrypt(encrypted_key_signature, private_key_receiver)

    is_valid_signature = Verify(decrypted_key_signature, decrypted_key, public_key_sender)

    if not is_valid_signature:
        return decrypted_key, "Підпис або ключ є недійсними."

    return decrypted_key, "Підпис і ключ є дійсними. Перевірка успішна."


if __name__ == "__main__":
    while True:
        # Генерація пар простих чисел для A
        public_key_a, private_key_a = GenerateKeyPair(256)

        # Генерація пар простих чисел для B
        public_key_b, private_key_b = GenerateKeyPair(256)

        # Перевірка умови pq ≤ p1q1
        if private_key_a[1] * private_key_a[2] <= private_key_b[1] * private_key_b[2]:
            break

    # Створення випадкового повідомлення для тесту
    message = generate_random_message(public_key_a[0])

    # Шифрування для A і B
    ciphertext_a = Encrypt(message, public_key_a)
    ciphertext_b = Encrypt(message, public_key_b)

    # Розшифрування для A і B
    decrypted_a = Decrypt(ciphertext_a, private_key_a)
    decrypted_b = Decrypt(ciphertext_b, private_key_b)

    # Створення цифрового підпису для A і B
    signature_a = Sign(message, private_key_a)
    signature_b = Sign(message, private_key_b)

    # Перевірка цифрового підпису
    is_valid_a = Verify(signature_a, message, public_key_a)
    is_valid_b = Verify(signature_b, message, public_key_b)

    # Випадковий ключ для передачі
    key_to_send = generate_random_message(public_key_a[0])

    # Відправлення ключа
    encrypted_key, encrypted_key_signature = SendKey(public_key_b, private_key_a, key_to_send)

    # Прийом ключа
    received_key, verify_message = ReceiveKey(encrypted_key, encrypted_key_signature, public_key_a, private_key_b)

    with open("rsa_results.txt", "w", encoding="UTF-8") as file:
        file.write(f"Перевірка шифрування, розшифрування, підпису, перевірки підпису\n")
        file.write(f"Відкритий ключ A: {public_key_a}\n")
        file.write(f"Секретний ключ A: {private_key_a}\n\n")
        file.write(f"Відкритий ключ B: {public_key_b}\n")
        file.write(f"Секретний ключ B: {private_key_b}\n\n")
        file.write(f"Оригінальне повідомлення: {message}\n\n")
        file.write(f"Зашифроване повідомлення для A: {ciphertext_a}\n")
        file.write(f"Зашифроване повідомлення для B: {ciphertext_b}\n\n")
        file.write(f"Розшифроване повідомлення для A: {decrypted_a}\n")
        file.write(f"Розшифроване повідомлення для B: {decrypted_b}\n\n")
        file.write(f"Цифровий підпис A: {signature_a}\n")
        file.write(f"Цифровий підпис B: {signature_b}\n\n")
        file.write(f"Перевірка цифрового підпису для A: {is_valid_a}\n")
        file.write(f"Перевірка цифрового підпису для B: {is_valid_b}\n\n\n")

        file.write(f"Перевірка відправлення та отримання ключа\n")
        file.write(f"Kлюч для передачі: {key_to_send}\n")
        file.write(f"Відправлені ключ та підпис: {encrypted_key, encrypted_key_signature}\n")
        file.write(f"Отриманий ключ: {received_key}\n")
        file.write(verify_message)