import random

def is_prime_miller_rabin(n, k=5):
    """Перевірка числа n на простоту тестом Міллера-Рабіна"""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
        if n == p:
            return True
        if n % p == 0:
            return False
        
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

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

def generate_prime_in_bit_range(min_bits, max_bits):
    """
    Генерує випадкове просте число у діапазоні бітів [min_bits, max_bits]
    """
    if min_bits < 2 or max_bits < min_bits:
        raise ValueError("Некоректний діапазон бітів.")
    
    while True:
        lower_bound = 1 << (min_bits - 1)  
        upper_bound = (1 << max_bits) - 1
        candidate = random.randint(lower_bound, upper_bound)
        candidate |= 1
        if is_prime_miller_rabin(candidate):
            return candidate

def generate_two_prime_pairs(min_bits=256, max_bits=256):
    """Генерує дві пари простих чисел p,q і p1,q1 з умовою pq <= p1q1"""
    while True:
        p = generate_prime_in_bit_range(min_bits, max_bits)
        q = generate_prime_in_bit_range(min_bits, max_bits)
        pq = p * q

        p1 = generate_prime_in_bit_range(min_bits, max_bits)
        q1 = generate_prime_in_bit_range(min_bits, max_bits)
        p1q1 = p1 * q1

        if pq <= p1q1:
            return (p, q), (p1, q1)

pair_A, pair_B = generate_two_prime_pairs()
p, q = pair_A
p1, q1 = pair_B

min_bits = 64
max_bits = 128
prime_number = generate_prime_in_bit_range(min_bits, max_bits)
print(f"Випадкове просте число у діапазоні {min_bits}-{max_bits} біт:\n{prime_number}")

print("Пара простих чисел для абонента A:")
print(f"p = {p}")
print(f"q = {q}")
print(f"Добуток pq = {p * q}")

print("\nПара простих чисел для абонента B:")
print(f"p1 = {p1}")
print(f"q1 = {q1}")
print(f"Добуток p1q1 = {p1 * q1}")