import random
from sympy import mod_inverse


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
    phi_n = (p - 1) * (q - 1)
    e = 65537  
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n)
    

    d = mod_inverse(e, phi_n)
    

    public_key = (e, n)
    private_key = (d, p, q)
    
    return public_key, private_key


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


public_key_a, private_key_a = generate_rsa_keys(bit_length=256)
public_key_b, private_key_b = generate_rsa_keys(bit_length=256)


print("Public key of A:", public_key_a)
print("Private key of A:", private_key_a)
print("Public key of B:", public_key_b)
print("Private key of B:", private_key_b)
