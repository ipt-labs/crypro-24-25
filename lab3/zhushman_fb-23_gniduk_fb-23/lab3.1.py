def extended_gcd(a, m):
    """
    Алгоритм Евкліда
    """
    if m == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(m, a % m)
    x = y1
    y = x1 - (a // m) * y1
    return gcd, x, y

def modular_inverse(a, m):
    """
    Знаходить обернений елемент a за модулем m.
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None  # Оберненого елемента не існує
    return x % m

def solve_linear_congruence(a, b, m):
    """
    Розв’язує лінійне порівняння ax ≡ b (mod m).
    Повертає список всіх розв’язків або повідомляє, якщо розв’язків немає.
    """
    gcd, x, _ = extended_gcd(a, m)
    if b % gcd != 0:
        return []  # Немає розв’язків
    # Знаходимо перший розв’язок
    x0 = (x * (b // gcd)) % m
    solutions = [(x0 + i * (m // gcd)) % m for i in range(gcd)]
    return solutions

while True:
    print("\n=== Виберіть операцію ===")
    print("1. Знайти обернений елемент (Евкліда)")
    print("2. Розв’язати лінійне порівняння ax ≡ b (mod m)")
    print("3. Вийти")
    choice = input("Ваш вибір: ")

    if choice == "1":
        a = int(input("Введіть a: "))
        m = int(input("Введіть модуль m: "))
        inverse = modular_inverse(a, m)
        if inverse is not None:
            print(f"Обернений елемент для {a} за модулем {m}: {inverse}")
        else:
            print(f"Обернений елемент для {a} за модулем {m} не існує")
    elif choice == "2":
        a = int(input("Введіть a: "))
        b = int(input("Введіть b: "))
        m = int(input("Введіть модуль m: "))
        solutions = solve_linear_congruence(a, b, m)
        if len(solutions) == 0:
            print("Немає розв’язків")
        elif len(solutions) == 1:
            print(f"Один розв’язок: x = {solutions[0]}")
        else:
            print(f"Кілька розв’язків: {', '.join(map(str, solutions))}")
    elif choice == "3":
        print("Вихід із програми.")
        break
    else:
        print("Невірний вибір. Спробуйте ще раз.")


