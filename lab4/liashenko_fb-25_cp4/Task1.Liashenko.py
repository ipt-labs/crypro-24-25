import random

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


min_value = 2**255
max_value = 2**256 - 1
prime = generate_random_prime(min_value, max_value)


if miller_rabin_test(prime):
    print(f"Prime number: {prime} is prime.")
else:
    print(f"Prime number: {prime} is not prime.")
