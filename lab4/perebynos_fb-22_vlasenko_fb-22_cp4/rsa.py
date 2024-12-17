from primes import get_rsa_prime
from helpers import gcd_extended_euclid, horner_pow
from random import randint

e = 65537

def _GenerateKeyPair(e: int, p: int, q: int) -> tuple[tuple[int, int], tuple[int, int, int]]:
    n = p*q
    phi = (p-1)*(q-1)
    gcd, d = gcd_extended_euclid(e, phi)
    if gcd != 1:
        raise ValueError(f"e={e} and phi={phi} are not coprime")
    
    return (e, n), (d, p, q)

def GenerateKeyPair(bits: int) -> tuple[tuple[int, int], tuple[int, int, int]]:
    p = get_rsa_prime(bits//2)
    q = get_rsa_prime(bits//2)

    return _GenerateKeyPair(e, p, q)

def Encrypt(plaintext: int, public_key: tuple[int, int]) -> int:
    return horner_pow(plaintext, public_key[0], public_key[1])

def Decrypt(ciphertext: int, private_key: tuple[int, int, int]) -> int:
    return horner_pow(ciphertext, private_key[0], private_key[1] * private_key[2])

def Sign(message: int, private_key: tuple[int, int, int]) -> int:
    return horner_pow(message, private_key[0], private_key[1] * private_key[2])

def Verify(message: int, signature: int, public_key: tuple[int, int]) -> bool:
    return horner_pow(signature, public_key[0], public_key[1]) == message

def SendKey(k: int, sender_private_key: tuple[int, int, int], receiver_public_key: tuple[int, int]) -> tuple[int, int]:
    sender_n = sender_private_key[1] * sender_private_key[2]
    receiver_n = receiver_public_key[1]

    if sender_n > receiver_n:
        raise ValueError(f"Sender's n={sender_n} is greater than receiver's n={receiver_n}")

    if k >= sender_n:
        raise ValueError(f"Key={k} is greater than sender's n={sender_n}")

    k_encrypted = Encrypt(k, receiver_public_key)
    k_signature = Sign(k, sender_private_key)
    k_signature_encrypted = Encrypt(k_signature, receiver_public_key)

    return k_encrypted, k_signature_encrypted

def ReceiveKey(sender_public_key: tuple[int, int], receiver_private_key: tuple[int, int, int], k_encrypted: int, k_signature_encrypted: int) -> tuple[int, bool]:
    sender_n = sender_public_key[1]
    receiver_n = receiver_private_key[1] * receiver_private_key[2]

    if sender_n > receiver_n:
        raise ValueError(f"Sender's n={sender_n} is greater than receiver's n={receiver_n}")

    k = Decrypt(k_encrypted, receiver_private_key)
    k_signature = Decrypt(k_signature_encrypted, receiver_private_key)

    return k, Verify(k, k_signature, sender_public_key)


def main():
    key_length = 512

    public_key, private_key = GenerateKeyPair(key_length)
    message = randint(2, public_key[1])
    print(f"Key length: {key_length}")
    print(f"Public key: {public_key}")
    print(f"Private key: {private_key}")
        
    print(f"\nMessage: {message}")

    print("\nTest RSA encryption and decryption:")
    encrypted = Encrypt(message, public_key)
    print(f"Encrypted: {encrypted}")

    decrypted = Decrypt(encrypted, private_key)
    print(f"Decrypted: {decrypted}")
    assert message == decrypted

    print("\nTest RSA signature and verification:")
    signature = Sign(message, private_key)
    print(f"Signature: {signature}")

    verified = Verify(message, signature, public_key)
    print(f"Verified: {verified}")
    assert verified

    print("\nTest RSA verification with wrong message:")
    verified = Verify(message+1, signature, public_key)
    print(f"Verified: {verified}")
    assert not verified

    print("\nAll tests passed!")

if __name__ == "__main__":
    main()
