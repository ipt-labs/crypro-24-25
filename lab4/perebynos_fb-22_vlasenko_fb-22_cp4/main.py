from rsa import GenerateKeyPair, Sign, Verify, Encrypt, Decrypt, ReceiveKey, SendKey
from primes import get_prime, get_rsa_prime
from random import randint


def main():
    key_length = 512

    public_key_A, private_key_A = GenerateKeyPair(key_length)
    public_key_B, private_key_B = GenerateKeyPair(key_length)
    print(f"Modulus length: {key_length}")
    print(f"\nA: p={private_key_A[1]}, q={private_key_A[2]}")
    while public_key_A[1] > public_key_B[1]:
        print(f"Invalid B: p={private_key_B[1]}, q={private_key_B[2]}")
        public_key_B, private_key_B = GenerateKeyPair(key_length)

    print(f"B: p={private_key_B[1]}, q={private_key_B[2]}")

    print(f"\nA public key: {public_key_A}")
    print(f"A private key: {private_key_A}")

    print(f"\nB public key: {public_key_B}")
    print(f"B private key: {private_key_B}")


    # Test RSA encryption and decryption
    print("\n\nTest RSA encryption and decryption:")
    message_A = randint(2, public_key_A[1])
    print(f"Message for A: {message_A}")

    encrypted_message_A = Encrypt(message_A, public_key_A)
    print(f"Encrypted message for A: {encrypted_message_A}")

    decrypted_message_A = Decrypt(encrypted_message_A, private_key_A)
    print(f"Decrypted message for A: {decrypted_message_A}")

    message_B = randint(2, public_key_B[1])
    print(f"\nMessage for B: {message_B}")

    encrypted_message_B = Encrypt(message_B, public_key_B)
    print(f"Encrypted message for B: {encrypted_message_B}")

    decrypted_message_B = Decrypt(encrypted_message_B, private_key_B)
    print(f"Decrypted message for B: {decrypted_message_B}")
        

    # Test RSA signature and verification
    print("\n\nTest RSA signature and verification:")
    message_A = randint(2, public_key_A[1])
    print(f"Message for A: {message_A}")
    signature_message_A = Sign(message_A, private_key_A)
    print(f"Signature by A: {signature_message_A}")
    decrypted_signature_message_A = Encrypt(signature_message_A, public_key_A) # because verifying is the same encryption
    print(f"Decrypted signature by A: {decrypted_signature_message_A}")
    verified_A = Verify(message_A, signature_message_A, public_key_A)
    print(f"Verified by A: {verified_A}")

    message_B = randint(2, public_key_B[1])
    print(f"\nMessage for B: {message_B}")
    signature_message_B = Sign(message_B, private_key_B)
    print(f"Signature by B: {signature_message_B}")
    decrypted_signature_message_B = Encrypt(signature_message_B, public_key_B) # because verifying is the same encryption
    print(f"Decrypted signature by B: {decrypted_signature_message_B}")
    verified_B = Verify(message_B, signature_message_B, public_key_B)
    print(f"Verified by B: {verified_B}")


    # Test RSA key sharing algorithm
    print("\n\nTest RSA key sharing algorithm:")
    k = randint(2, public_key_A[1])
    print(f"Key: {k}")
    print(f"\nSending:")
    k_encrypted = Encrypt(k, public_key_B)
    print(f"Encrypted key: {k_encrypted}")
    k_signature = Sign(k, private_key_A)
    print(f"Key signature: {k_signature}")
    k_signature_encrypted = Encrypt(k_signature, public_key_B)
    print(f"Encrypted key signature: {k_signature_encrypted}")

    print(f"\nReceiving:")
    k = Decrypt(k_encrypted, private_key_B)
    print(f"Decrypted key: {k}")
    k_signature = Decrypt(k_signature_encrypted, private_key_B)
    print(f"Decrypted key signature: {k_signature}")
    decrypted_k_signature = Encrypt(k_signature, public_key_A) # because verifying is the same encryption
    print(f"Decrypted key signature by A: {decrypted_k_signature}")
    print(f"Verified: {Verify(k, k_signature, public_key_A)}")


if __name__ == "__main__":
    main()
