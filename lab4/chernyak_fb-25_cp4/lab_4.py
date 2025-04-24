import random
from sympy import gcd


def is_prime(n, k=10):
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
        x = pow(a, d, n)  # a^d % n
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_random_prime(bit_length):
    candidates = []
    while True:
        candidate = random.getrandbits(bit_length) | (1 << (bit_length - 1)) | 1
        if is_prime(candidate):
            return candidate, candidates
        candidates.append(candidate)


def generate_prime_pairs(bit_length=256):
    while True:
        p, p_candidates = generate_random_prime(bit_length)
        q, q_candidates = generate_random_prime(bit_length)
        if p * q < generate_random_prime(bit_length * 2)[0]:
            return p, q, p_candidates, q_candidates


def generate_rsa_keys(bit_length=256):
    p, q, p_candidates, q_candidates = generate_prime_pairs(bit_length)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    print(f"Значення p: {p}")
    print(f"Значення q: {q}")
    print(f"Значення n: {n}")
    print(f"Значення phi(n): {phi_n}")

    e = 65537
    if gcd(e, phi_n) != 1:
        raise ValueError("e і phi_n не взаємно прості!")

    d = pow(e, -1, phi_n)

    return (e, n), (d, p, q), p_candidates, q_candidates


def encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)


def decrypt(ciphertext, private_key):
    d, p, q = private_key
    n = p * q
    return pow(ciphertext, d, n)


def sign(message, private_key):
    d, p, q = private_key
    n = p * q
    return pow(message, d, n)


def verify(signature, message, public_key):
    e, n = public_key
    return pow(signature, e, n) == message


if __name__ == "__main__":
    public_key_A, private_key_A, p_candidates_A, q_candidates_A = generate_rsa_keys()
    public_key_B, private_key_B, p_candidates_B, q_candidates_B = generate_rsa_keys()

    print("Публічний ключ A:", public_key_A)
    print("Приватний ключ A:", private_key_A)
    print("Публічний ключ B:", public_key_B)
    print("Приватний ключ B:", private_key_B)

    print("Кандидати на p для A, що не пройшли перевірку простоти:", p_candidates_A)
    print("Кандидати на q для A, що не пройшли перевірку простоти:", q_candidates_A)
    print("Кандидати на p для B, що не пройшли перевірку простоти:", p_candidates_B)
    print("Кандидати на q для B, що не пройшли перевірку простоти:", q_candidates_B)

    message = random.randint(1, public_key_A[1] - 1)
    print("Відкрите повідомлення M:", message)

    signature = sign(message, private_key_A)
    print("Цифровий підпис A:", signature)

    encrypted_message = encrypt(message, public_key_B)
    encrypted_signature = encrypt(signature, public_key_B)
    print("Зашифроване повідомлення:", encrypted_message)
    print("Зашифрований підпис:", encrypted_signature)

    decrypted_message = decrypt(encrypted_message, private_key_B)
    decrypted_signature = decrypt(encrypted_signature, private_key_B)
    print("Розшифроване повідомлення B:", decrypted_message)
    print("Розшифрований підпис B:", decrypted_signature)

    is_valid = verify(decrypted_signature, decrypted_message, public_key_A)
    print("Валідність підпису B:", is_valid)
