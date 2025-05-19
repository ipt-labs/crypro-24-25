import random
from math import gcd


def miller_rabin(n, k=40):
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

    
    for m in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for m in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_r_prime(bit_length):
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1  
        if miller_rabin(candidate):
            return candidate


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_val, x, y


def generate_rsa_keys(bit_length=256):
    
    p = generate_r_prime(bit_length)
    q = generate_r_prime(bit_length)

    
    n = p * q
    phi_n = (p - 1) * (q - 1)

   
    while True:
        e = random.randint(17, phi_n - 1)
        if gcd(e, phi_n) == 1:
            break

   
    _, d, _ = extended_gcd(e, phi_n)
    d = d % phi_n
    if d < 0:
        d += phi_n

    
    public_key = (e, n)
    private_key = (d, p, q)
    return public_key, private_key


public_key_a, private_key_a = generate_rsa_keys(256)
public_key_b, private_key_b = generate_rsa_keys(256)


print("Відкритий ключ для абонента A:", public_key_a)
print("Секретний ключ для абонента A:", private_key_a)
print("\nВідкритий ключ для абонента B:", public_key_b)
print("Секретний ключ для абонента B:", private_key_b)
