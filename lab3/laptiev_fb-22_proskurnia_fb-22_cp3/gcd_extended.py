# Розширений алгоритм Евкліда
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Знаходимо обернений елемент
def find_inverse(a, mod):
    gcd, x, _ = gcd_extended(a, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    return -1

# Розв'язання лінійних рівнянь
def solve_equation(a, b, mod):
    gcd, x, _ = gcd_extended(a, mod)
    if gcd == 1:
        return (find_inverse(a, mod) * b) % mod
    if b % gcd != 0:
        return -1
    a1, b1, n1 = a // gcd, b // gcd, mod // gcd
    x0 = solve_equation(a1, b1, n1)
    return int(x0)

# Функція= для демонстрації роботи програми вище, задаємо випадкові значення
def main():
    a = 3
    b = 1  
    mod = 11
    gcd, x, y = gcd_extended(a, mod)
    print(f"НСД({a}, {mod}) = {gcd}, x = {x}, y = {y}")
    inverse = find_inverse(a, mod)
    print(f"Обернений елемент {a} за модулем {mod} = {inverse if inverse != -1 else 'немає'}")
    solution = solve_equation(a, b, mod)
    print(f"Розв'язок рівняння {a}x ≡ {b} (mod {mod}) = {solution if solution != -1 else 'немає розв_язку'}")

if __name__ == "__main__":
    main()