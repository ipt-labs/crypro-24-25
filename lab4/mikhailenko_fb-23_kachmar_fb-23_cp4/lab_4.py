import random
from sympy import gcd


def is_prime(num, k=10):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0:
        return False

    r, d = 0, num - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, num - 2)
        x = pow(a, d, num)
        if x == 1 or x == num - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False

    return True


def generate_random_prime(bit_len):
    candidates = []
    while True:
        candidate = random.getrandbits(bit_len) | (1 << (bit_len - 1)) | 1
        if is_prime(candidate):
            return candidate, candidates
        candidates.append(candidate)


def generate_prime_pairs(bit_len=256):
    while True:
        prime1, prime1_candidates = generate_random_prime(bit_len)
        prime2, prime2_candidates = generate_random_prime(bit_len)
        if prime1 * prime2 < generate_random_prime(bit_len * 2)[0]:
            return prime1, prime2, prime1_candidates, prime2_candidates


def generate_rsa_keys(bit_len=256):
    prime1, prime2, prime1_candidates, prime2_candidates = generate_prime_pairs(bit_len)
    modulus = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)

    print(f"Prime p: {prime1}")
    print(f"Prime q: {prime2}")
    print(f"Modulus n: {modulus}")
    print(f"Euler's totient phi(n): {phi}")

    e = 65537
    if gcd(e, phi) != 1:
        raise ValueError("e and phi(n) are not coprime!")

    d = pow(e, -1, phi)

    return (e, modulus), (d, prime1, prime2), prime1_candidates, prime2_candidates


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
    public_key_A, private_key_A, candidates_p_A, candidates_q_A = generate_rsa_keys()
    public_key_B, private_key_B, candidates_p_B, candidates_q_B = generate_rsa_keys()

    print("Public key A:", public_key_A)
    print("Private key A:", private_key_A)
    print("Public key B:", public_key_B)
    print("Private key B:", private_key_B)

    print("Candidates for p in A that failed primality test:", candidates_p_A)
    print("Candidates for q in A that failed primality test:", candidates_q_A)
    print("Candidates for p in B that failed primality test:", candidates_p_B)
    print("Candidates for q in B that failed primality test:", candidates_q_B)

    random_message = random.randint(1, public_key_A[1] - 1)
    print("Random message M:", random_message)

    digital_signature = sign(random_message, private_key_A)
    print("Digital signature by A:", digital_signature)

    encrypted_message = encrypt(random_message, public_key_B)
    encrypted_signature = encrypt(digital_signature, public_key_B)
    print("Encrypted message for B:", encrypted_message)
    print("Encrypted signature for B:", encrypted_signature)

    decrypted_message = decrypt(encrypted_message, private_key_B)
    decrypted_signature = decrypt(encrypted_signature, private_key_B)
    print("Decrypted message by B:", decrypted_message)
    print("Decrypted signature by B:", decrypted_signature)

    is_valid_signature = verify(decrypted_signature, decrypted_message, public_key_A)
    print("Signature validity verified by B:", is_valid_signature)
