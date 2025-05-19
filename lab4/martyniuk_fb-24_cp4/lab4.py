import random
import hashlib
import hexdump
import requests

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def trial_division(n):
    if n < 2:
        return False
    for i in range(2, 100):
        if n % i == 0:
            return False
    return True

def miller_rabin_test(p, k=10):
    if p < 2:
        return False
    if p != 2 and p % 2 == 0:
        return False

    factorization_base = p - 1
    while factorization_base % 2 == 0:
        factorization_base //= 2

    for _ in range(k):
        witness = random.randint(1, p - 1)
        if gcd(witness, p) > 1:
            continue

        exponent = factorization_base
        residue = pow(witness, exponent, p)

        while exponent != p - 1 and residue != 1 and residue != p - 1:
            residue = (residue * residue) % p
            exponent *= 2

        if residue != p - 1 and exponent % 2 == 0:
            return False

    return True

#Debug 
'''
p = [659, 600, 359, 14]
for i in p:
    result = miller_rabin_test(i)
    if result: print(f"\n{i} сильно псевдопросте\n")
    else: print(f"\n{i} складене число\n")
'''

def generate_random_prime(start, end, k=10):
    while True:
        p = random.randint(start, end)
        if trial_division(p) and miller_rabin_test(p, k):
            return p


#Debug 
'''
for _ in range(4):
    print("\n",generate_random_prime(1337, 8120),"\n")
'''

def GenerateKeyPairs():
    bit_length = 256

    primes = [generate_random_prime(2**(bit_length-1), 2**bit_length - 1) for _ in range(4)]

    primes.sort()

    p, q = primes[:2]
    p1, q1 = primes[2:]

    return p, q, p1, q1


#Debug
'''
p, q, p1, q1 = GenerateKeyPairs()
print(f"\nAlice's public key: ({p}, {q})")
print(f"Bob's public key: ({p1}, {q1})\n")
if p*q <= p1*q1: print("pq <= p1q1\n")
'''


def GenerateRsaKeys(p, q, p1, q1):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    while True:
        public_exponent = random.randint(2, phi_n - 1)
        gcd_result, _, private_exponent = extended_gcd(phi_n, public_exponent)
        if gcd_result == 1:
            break

    n1 = p1 * q1
    phi_n1 = (p1 - 1) * (q1 - 1)

    while True:
        public_exponent_1 = random.randint(2, phi_n1 - 1)
        gcd_result_1, _, private_exponent_1 = extended_gcd(phi_n1, public_exponent_1)
        if gcd_result_1 == 1:
            break

    public_key = (n, public_exponent)
    private_key = (private_exponent, p, q)

    public_key_1 = (n1, public_exponent_1)
    private_key_1 = (private_exponent_1, p1, q1)

    return public_key, private_key, public_key_1, private_key_1


#Debug
p, q, p1, q1 = GenerateKeyPairs()
alice_public_key, alice_private_key, bob_public_key, bob_private_key = GenerateRsaKeys(p, q, p1, q1)
print("\nAlice's RSA public pey:", alice_public_key)
print("Alice's RSA private key:", alice_private_key)
print("Bob's RSA public key:", bob_public_key)
print("Bob's RSA private key:", bob_private_key,"\n")


def Encrypt(M_, pubkey):
    if not isinstance(M_, int):
        M_ = int.from_bytes(M_.encode('utf-8'), byteorder='big')

    if 0 <= M_ <= pubkey[0] - 1:
        C_ = pow(M_, pubkey[1], pubkey[0])
        return C_
    else:
        return None

def Decrypt(C_, privkey, text=False):
    n_ = privkey[1] * privkey[2]

    if 0 <= C_ <= n_ - 1:
        M_ = pow(C_, privkey[0], n_)

        if text:
            return M_.to_bytes((M_.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
        else:
            return M_
    else:
        return None


def Sign(message, private_key):
    d, p, q = private_key
    n = p * q

    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')

    signature = pow(message_int, d, n)
    return (message.encode('utf-8').hex(), signature)

def Verify(signed_message, public_key):
    message, signature = signed_message
    n, e = public_key
    if not isinstance(signature, int):
        signature = int(signature, 16)

    message_bytes = bytes.fromhex(message)
    message_int = int.from_bytes(message_bytes, byteorder='big')

    decrypted_signature = pow(signature, e, n)

    return decrypted_signature == message_int

def SendKey(public_key_B, private_key_A, public_key_A):
    k = random.randint(0, public_key_A[0] - 1)
    print("\nk value:", k)
    s = pow(k, private_key_A[0], public_key_A[0])
    k_1 = pow(k, public_key_B[1], public_key_B[0])
    S_1 = pow(s, public_key_B[1], public_key_B[0])
    return k_1, S_1

def RecieveKey(k_1, S_1, public_key_B, private_key_B, public_key_A):
    k = pow(k_1, private_key_B[0], public_key_B[0])
    S = pow(S_1, private_key_B[0], public_key_B[0])
    return k == pow(S, public_key_A[1], public_key_A[0])



p, q, p1, q1 = GenerateKeyPairs()
alice_public_key, alice_private_key, bob_public_key, bob_private_key = GenerateRsaKeys(p, q, p1, q1)

message_to_alice = str(random.randint(812, 2014)) 
cipher_text_for_alice = Encrypt(message_to_alice, alice_public_key)
print(cipher_text_for_alice)
Decrypted_message_for_alice = Decrypt(cipher_text_for_alice, alice_private_key, text=True)

message_to_bob = "Hello, Bob!"
signed_message_for_bob = Sign(message_to_bob, bob_private_key)
signature_verified = Verify(signed_message_for_bob, bob_public_key)

k_1, S_1 = SendKey(bob_public_key, alice_private_key, alice_public_key)
key_received = RecieveKey(k_1, S_1, bob_public_key, bob_private_key, alice_public_key)

print("\nMessage to Alice:", message_to_alice)
print("Encrypted Cipher Text for Alice:", cipher_text_for_alice)
print("Decrypted Message for Alice:", Decrypted_message_for_alice, "\n")

print("Message to Bob:", message_to_bob)
print("Signed Message for Bob:", signed_message_for_bob)
print("Signature Verification Result for Bob:", signature_verified, "\n")


if key_received:
    print("Key exchange successful!")
else:
    print("Key exchange failed!")



#Testing environment
print("\n\n\n==Testing environment==\n")
s = requests.Session()
url = "http://asymcryptwebservice.appspot.com/rsa/"

#Encryption

#Getting public key from server
payload = {'keySize': '256'}
r_serverKey= s.get(url+"serverKey", params=payload)
server_pub_key = (int(r_serverKey.json()['modulus'], 16), int(r_serverKey.json()['publicExponent'], 16))
print("Server's public key:")
print(r_serverKey.json(), '\n')

message_to_server = 'hello1488' 
print('Message:', message_to_server+'\n')


#Encrypting message with my implementation
cipher_text_for_server = Encrypt(message_to_server, server_pub_key)
print("My cipher text for server:        ", hex(cipher_text_for_server)[2:])


#Encrypting message with server's implementation
payload = {'modulus': r_serverKey.json()['modulus'], 'publicExponent': r_serverKey.json()['publicExponent'], 'message': message_to_server.encode('utf-8').hex()}
r_encrypt = s.get(url+"encrypt", params=payload)
print("Cipher text generated by server:  ", r_encrypt.json()['cipherText'])


#Decrypting my cipher text using server 
print('\nSending cipher text generated by server...')
payload = {'cipherText': r_encrypt.json()['cipherText'], 'expectedType' : 'BYTES'}
r = s.get(url+"decrypt", params=payload)
print("Decrypted bytes:")
hexdump.hexdump(bytes.fromhex(r.json()['message']))


#Decrypting server's cipher text using server 
print('\nSending my cipher text...')
payload = {'cipherText': hex(cipher_text_for_server)[2:], 'expectedType' : 'BYTES'}
r = s.get(url+"decrypt", params=payload)
print("Decrypted bytes:")
hexdump.hexdump(bytes.fromhex(r.json()['message']))


#Signing
message_server = "kitty" 
print("\n\nMessage: ", message_server)

print("\nServer signing message...")
payload = {'message': message_server.encode('utf-8').hex(),'expectedType': 'BYTES'}
r = s.get(url+"sign", params=payload)
signature = r.json()['signature']
print("Server's signature:", r.json()['signature'])

print("Veryfing with server public key...")
verified = Verify((message_server.encode('utf-8').hex(), signature), server_pub_key)
print(verified)


message_bob = "Disintegration"
print("\nMessage: ", message_bob)
print("\nBob signing the message...")
message_bob_bytes, signature_bob = Sign(message_bob, bob_private_key)
print(f"Signature: {hex(signature_bob)[2:]}")


print("Sending message with public key and signature to server...")
payload = {'modulus': hex(bob_public_key[0])[2:], 'publicExponent': hex(bob_public_key[1])[2:], 'message': message_bob.encode('utf-8').hex(), 'signature': hex(signature_bob)[2:]}
r = s.get(url+"verify", params=payload)
print("Server response:", r.json())



