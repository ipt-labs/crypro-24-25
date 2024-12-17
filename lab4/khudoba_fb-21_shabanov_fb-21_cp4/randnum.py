import random
import math

# Пробне ділення
def trial_division(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = int(math.sqrt(n)) + 1
    for i in range(5, limit, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

# Тест Міллера-Рабіна
def miller_rabin(p, k=5):
    if p == 2 or p == 3:
        return True
    if p < 2 or p % 2 == 0:
        return False

    # Крок 0: розклад p-1 = d * 2^s
    s, d = 0, p - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Крок 1: k раундів перевірок
    for _ in range(k):
        x = random.randint(2, p - 2)  # вибір випадкової основи
        g = gcd(x, p)

        # Якщо x і p не взаємно прості, то p складене
        if g != 1:
            return False

        # Крок 2: перевірка сильної псевдопростоти
        x_power = pow(x, d, p)  # x^d mod p
        if x_power == 1 or x_power == p - 1:
            continue

        for r in range(s - 1):
            x_power = pow(x_power, 2, p)  # x^(2^r * d) mod p
            if x_power == p - 1:
                break
        else:
            return False  # Якщо не знайдено псевдопростоти, p складене

    return True  # Якщо p пройшло всі k раундів, воно, ймовірно, просте

# Евклідовий алгоритм для знаходження найбільшого спільного дільника (gcd)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Швидша генерація простих чисел
def random_prime_by_length(length):
    while True:
        p = random.getrandbits(length) | 1  # генеруємо непарне число
        if miller_rabin(p):
            return p

# Генерація випадкового простого числа
bit_length = 256
prime_number_by_length = random_prime_by_length(bit_length)

print(f"Випадкове просте число з {bit_length} біт: {prime_number_by_length}")
