import random


def gcd(a, b):
    """Обчислення найбільшого спільного дільника (НСД)."""
    while b:
        a, b = b, a % b
    return a


def extended_euclid(a, b):
    """
    Розширений алгоритм Евкліда для знаходження найбільшого спільного дільника та коефіцієнтів
    рівняння Безу для ax + by = gcd(a, b)
    Повертає кортеж (gcd, x, y), де gcd — найбільший спільний дільник a та b,
    x і y — коефіцієнти рівняння Безу.
    """
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_euclid(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(a, m):
    """
    Знаходить обернений елемент a за модулем m.
    Повертає обернений елемент, якщо він існує (тобто a і m взаємно прості),
    інакше повертає None.
    """
    gcd, x, _ = extended_euclid(a, m)
    if gcd != 1:
        return None
    return x % m


def modular_pow(base, exp, mod):
    """
    Обчислення (base^exp) % mod за допомогою алгоритму бінарного піднесення до степеня.

    :param base: Основа (число, яке підносимо до степеня).
    :param exp: Показник степеня (експонента).
    :param mod: Модуль (для операції за модулем).
    :return: Результат обчислення (base^exp) % mod.
    """
    result = 1  # Початковий результат
    base = base % mod  # Зменшення основи за модулем

    while exp > 0:
        # Якщо поточний степінь непарний, множимо результат на основу
        if exp % 2 == 1:
            result = (result * base) % mod

        # Підносимо основу до квадрата
        base = (base * base) % mod

        # Зменшуємо показник степеня вдвічі
        exp //= 2

    return result


def is_prime_trial_division(n, small_primes):
    """Перевірка на простоту пробними діленнями."""
    if n < 2:
        return False
    for p in small_primes:
        if n % p == 0:
            return n == p
    return True


def miller_rabin_test(p, k=20):
    """
    Виконує імовірнісний тест Міллера-Рабіна для перевірки числа p на простоту.
    :param p: Число для перевірки
    :param k: Кількість ітерацій
    :return: True, якщо p є простим, інакше False
    """
    # Тривіальні перевірки
    if p <= 1:
        return False
    if p <= 3:
        return True
    if p % 2 == 0:
        return False

    # Крок 0: Розклад p-1 = d * 2^s
    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Допоміжна функція для на сильну псевдопростоту за основою x
    def is_strong_pseudoprime(x):
        """
        Перевіряє, чи є p сильно псевдопростим за основою x.
        :param x: Випадкова основа
        :return: True, якщо p є сильно псевдопростим за основою x
        """
        # Обчислюємо x^d mod p
        x = modular_pow(x, d, p)
        if x == 1 or x == p - 1:
            return True

        # Повторне зведення в квадрат до s-1 разів
        for _ in range(s - 1):
            x = modular_pow(x, 2, p)
            if x == p - 1:
                return True
            if x == 1:
                return False

        return False

    # Основний алгоритм
    for _ in range(k):
        # Крок 1: Вибір випадкової основи x
        x = random.randint(2, p - 2)

        # Якщо НСД(x, p) > 1, то p складене
        if gcd(x, p) > 1:
            return False

        # Крок 2: Перевірка на сильну псевдопростоту за основою x
        if not is_strong_pseudoprime(x):
            return False

    return True  # Якщо всі k перевірок пройдено, вважаємо p простим


def generate_random_prime(start, end):
    """Генерація випадкового простого числа у заданому інтервалі."""
    # Список малих простих чисел для пробного ділення
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    while True:
        # Генерація випадкового числа в заданому інтервалі
        candidate = random.randint(start, end)

        # Перевірка пробними діленнями
        if not is_prime_trial_division(candidate, small_primes):
            continue

        # Перевірка тестом Міллера-Рабіна
        if miller_rabin_test(candidate):
            return candidate


def generate_prime_pair(bits):
    """Генерація пари простих чисел з заданою довжиною."""
    p = generate_random_prime(2**(bits-1), 2**bits - 1)
    q = generate_random_prime(2**(bits-1), 2**bits - 1)
    return p, q


def generate_random_message(n):
    """Генерація випадкового повідомлення"""
    return random.randint(2, n)
