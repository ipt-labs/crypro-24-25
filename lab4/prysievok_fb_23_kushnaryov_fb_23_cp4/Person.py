import rsa

class Person:
    def __init__(self,name, bit_size=256):
        # Generate key pairs
        prime1, prime2 = rsa.generate_key_pairs(size=bit_size)[0]
        self.name = name
        self.public_key, self.private_key = rsa.rsa_key_generation(prime1, prime2)
        self.friends_public_key = None

    def send_message(self, message):
        encrypted_message = rsa.encrypt(message, self.friends_public_key)  # Encrypt message
        signature = rsa.sign_message(message, self.private_key)  # Create signature
        return encrypted_message, signature

    def receive_message(self, encrypted_message, signature):
        # Decrypt the message
        decrypted_message = rsa.decrypt(encrypted_message, self.private_key)

        # Verify the signature
        is_valid = rsa.verify_signature(decrypted_message, signature, self.friends_public_key)
        if not is_valid:
            return None

        # Return the decrypted message as a string
        return decrypted_message
    
    def take_friends_key(self, public_key):
        self.friends_public_key = public_key

