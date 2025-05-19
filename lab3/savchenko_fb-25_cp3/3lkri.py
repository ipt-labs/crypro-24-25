
def extendedev(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extendedev(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y


def modin(a, m):
    g, x, y = extendedev(a, m)
    if g != 1:
        return -1  
    else:
        return x % m  


def solve_linear_congruence(a, b, m):
    g, x, y = extendedev(a, m)
    solutions = []

    if b % g != 0:
        return solutions  

     
    a //= g
    b //= g
    m //= g

    
    inv = modin(a, m)
    if inv == -1:
        return solutions

    
    x0 = (inv * b) % m

    
    for i in range(g):
        solutions.append((x0 + i * m) % m)

    return solutions

def main():
    
    a, m = map(int, input("Введіть число та модуль для обчислення оберненого елементу (a m): ").split())
    inv = modin(a, m)
    if inv != -1:
        print(f"{a}^(-1) mod {m}: {inv}")
    else:
        print(f"Обернений елемент для {a} не існує за модулем {m}.")
    
    
    a, b, m = map(int, input("Введіть коефіцієнт a, праву частину b та модуль m для лінійного порівняння (a b m): ").split())
    solutions = solve_linear_congruence(a, b, m)
    if solutions:
        print(f"{a}x = {b} mod {m}: {', '.join(map(str, solutions))}")
    else:
        print(f"Розв'язку для {a}x = {b} mod {m} немає.")

if __name__ == "__main__":
    main()
