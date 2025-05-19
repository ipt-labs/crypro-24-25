from random import randint

from primes import select_two_primes_pairs
from rsa import Caller

N0 = 2 ** 256
N1 = 2 ** 257
LAB4_PATH = "..\\lab4\\"

p, q, p1, q1 = select_two_primes_pairs(N0, N1)
a = Caller("A", p, q, keystore=LAB4_PATH)
a.save_own_public_key()
a.save_own_secret_key()

b = Caller("B", p1, q1, keystore=LAB4_PATH)
b.save_own_public_key()
b.save_own_secret_key()

message = randint(1, N0)
print(f"message = {message}")
ae, an = a.get_public_key()
be, bn = b.get_public_key()

# encrypt / decrypt
encrypted = a.encrypt(message, be, bn)
print(f"encrypted={encrypted}")
message1 = b.decrypt(encrypted)
print(f"decrypted={message1}")

# sign / verify signature
message, signature = a.sign(message)
print(f"Verified signature: {b.verify(message, signature, ae, an)}")

# send / receive key
k = randint(1, N0)
print(f"Key to send:  {k}")
k1, s1 = a.send_key(k, be, bn)
kk = b.receive_key(k1, s1, ae, an)
print(f"Key received: {kk}")
