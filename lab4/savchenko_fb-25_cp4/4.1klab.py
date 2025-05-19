import random


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
        a = random.randint(17, n - 2)
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


def generate_r_prime(bit_l):
    while True:
        candidate = random.getrandbits(bit_l)
        candidate |= (1 << (bit_l - 1)) | 1  
        if miller_rabin(candidate):
            return candidate


def generate_pairs(bit_l=256):
    p = generate_r_prime(bit_l)
    q = generate_r_prime(bit_l)
    p1 = generate_r_prime(bit_l)
    q1 = generate_r_prime(bit_l)

    
    while p * q > p1 * q1:
        p1 = generate_r_prime(bit_l)
        q1 = generate_r_prime(bit_l)

    return (p, q), (p1, q1)


bit_l = 256
pair_a, pair_b = generate_pairs(bit_l)


p, q = pair_a
p1, q1 = pair_b

print("Пара для A:")
print(f"Число p: {p} (Розмір: {p.bit_length()} біт), Просте? {miller_rabin(p)}")
print(f"Число q: {q} (Розмір: {q.bit_length()} біт), Просте? {miller_rabin(q)}")

print("\nПара для B:")
print(f"Число p1: {p1} (Розмір: {p1.bit_length()} біт), Просте? {miller_rabin(p1)}")
print(f"Число q1: {q1} (Розмір: {q1.bit_length()} біт), Просте? {miller_rabin(q1)}")
