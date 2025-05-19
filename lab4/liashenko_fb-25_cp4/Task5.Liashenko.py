import random
import sympy


def miller_rabin_test(n, k=5):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
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

def generate_random_prime(min_value, max_value, bit_length=256):
    while True:
        candidate = random.getrandbits(bit_length)
        if min_value <= candidate <= max_value and miller_rabin_test(candidate):
            return candidate


def generate_rsa_keys(bit_length=256):
    p = generate_random_prime(2**(bit_length-1), 2**bit_length)
    q = generate_random_prime(2**(bit_length-1), 2**bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  
    d = pow(e, -1, phi)  
    return ((e, n), (d, p, q))


def encrypt_message(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]


def decrypt_message(encrypted_message, private_key):
    d, p, q = private_key
    n = p * q
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])


def create_digital_signature(message, private_key):
    d, p, q = private_key
    n = p * q
    message_hash = hash(message)
    return pow(message_hash, d, n)


def verify_digital_signature(message, signature, public_key):
    e, n = public_key
    message_hash = hash(message)
    return message_hash == pow(signature, e, n)


def generate_key_pair():
    return generate_rsa_keys()


def Encrypt(message, public_key):
    return encrypt_message(message, public_key)


def Decrypt(encrypted_message, private_key):
    return decrypt_message(encrypted_message, private_key)


def Sign(message, private_key):
    return create_digital_signature(message, private_key)


def Verify(message, signature, public_key):
    return verify_digital_signature(message, signature, public_key)


def SendKey(sender_private_key, receiver_public_key, shared_key):
    encrypted_key = Encrypt(str(shared_key), receiver_public_key)
    signature = Sign(str(shared_key), sender_private_key)
    return encrypted_key, signature


def ReceiveKey(encrypted_key, signature, sender_public_key, receiver_private_key):
    shared_key = Decrypt(encrypted_key, receiver_private_key)
    is_valid = Verify(str(shared_key), signature, sender_public_key)
    return shared_key, is_valid


bit_length = 256
public_key_A, private_key_A = generate_rsa_keys(bit_length)
public_key_B, private_key_B = generate_rsa_keys(bit_length)


shared_key = random.getrandbits(256)


encrypted_key, signature = SendKey(private_key_A, public_key_B, shared_key)
print(f"Encrypted key for B: {encrypted_key}")
print(f"Signature for key: {signature}")


received_key, is_valid = ReceiveKey(encrypted_key, signature, public_key_A, private_key_B)
print(f"Received key: {received_key}")
print(f"Signature valid: {is_valid}")
