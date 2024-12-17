def extended_euclidean(a, n):
    r0, r1 = a, n

    while True:
        gcd, _, _ = extended_euclidean_core(r0, r1)
        if gcd == 1:
            break
        r0 //= gcd
        r1 //= gcd

    gcd, u, v = extended_euclidean_core(r0, r1)

    if gcd != 1:
        raise ValueError("Обернений елемент не існує, оскільки gcd(a, n) ≠ 1.")

    b = u % n

    if ((a * b) - 1) % n == 0:
        #print(f"{a} * {b} - 1 ≡ 0 (mod {n}) - Перевірка успішна:D")
        return b
    else:
        #print(f"({a} * {b} - 1) не дорівнює 0 за модулем {n} - Перевірка не пройдена:(")
        return

def extended_euclidean_core(a, b):
    r0, r1 = a, b
    u0, u1 = 1, 0
    v0, v1 = 0, 1

    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1

    return r0, u0, v0

def solve_linear_congruence(a, b, n):
    gcd, u, _ = extended_euclidean_core(a, n)

    if gcd == 1:
        x = (u * b) % n
        return [x]

    elif gcd > 1:
        if b % gcd != 0:
            return []

        a1, b1, n1 = a // gcd, b // gcd, n // gcd

        _, u1, _ = extended_euclidean_core(a1, n1)
        x0 = (u1 * b1) % n1

        solutions = [(x0 + i * n1) % n for i in range(gcd)]
        return solutions
