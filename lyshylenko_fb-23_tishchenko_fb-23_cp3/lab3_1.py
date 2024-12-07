def GCD(a, b):                                           #Обчислення НСД
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = GCD(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def ModularInverse(a, m):                                #Обчислення a^-1

    gcd, x, _ = GCD(a, m)
    if gcd != 1:
        raise ValueError(f"Обернений елемент для {a} за модулем {m} не існує")
    return x % m


def LinearCongruence(a, b, m):                           #Лінійне порівняння ax ≡ b (mod m)
    gcd, x, _ = GCD(a, m)
    if b % gcd != 0:
        return []                                        # Розв'язків немає

    x0 = (x * (b // gcd)) % m                            #знаходимо один частковий розв'язок
    if x0 < 0:
        x0 += m

    solutions = []                                       #знаходимо всі розв'язки
    step = m // gcd
    for i in range(gcd):
        solutions.append((x0 + i * step) % m)

    return solutions


def main_menu():
    while True:
        print("\nОберіть опцію:")
        print("1. Обчислити обернений елемент за модулем")
        print("2. Розв'язати лінійне порівняння")
        print("3. Завершити програму")
        choice = input("-->: ")

        if choice == '1':                                # Обчислення оберненого елементу
            try:
                a = int(input("Введіть число a: "))
                m = int(input("Введіть модуль m: "))
                result = ModularInverse(a, m)
                print(f"Обернений елемент числа {a} за модулем {m}: a^-1= {result}")
            except ValueError as e:
                print(e)
        elif choice == '2':                              # Розв'язання лінійного порівняння
            a = int(input("Введіть коефіцієнт a: "))
            b = int(input("Введіть число b: "))
            m = int(input("Введіть модуль m: "))
            solutions = LinearCongruence(a, b, m)
            if solutions:
                print(f"Розв'язки лінійного порівняння {a}x ≡ {b} (mod {m}): {solutions}")
            else:
                print("Розв'язків немає")
        elif choice == '3':
            print("Програму завершено. Успіхів!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main_menu()
