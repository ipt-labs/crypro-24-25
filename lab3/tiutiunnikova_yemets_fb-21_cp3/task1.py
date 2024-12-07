#-------АЛГОРИТМ ЕВКЛІДА------------------------
def gcd_evc(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = gcd_evc(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

#-------ОБЕРНЕНИЙ ЗА МОДУЛЕМ------------------------
def obratn(a, m):
    gcd, x, _ = gcd_evc(a, m)
    if gcd != 1:
        return None  
    return x % m 

#-------ЛІНІЙНІ ПОРІВНЯННЯ------------------------
def congr(a, b, m):
    gcd, x, y = gcd_evc(a, m)    
    if b % gcd != 0:
        return []   
    a_ = a // gcd
    b_ = b // gcd
    m_ = m // gcd
    
    obratn_a = obratn(a_, m_)   
    if obratn_a is None:
        return []
    
    x0 = (obratn_a * b_) % m_
    answers = []
    for i in range(gcd):
        answers.append(x0 + i * m_)   
    return answers

#-------ПРИКЛАД 1 (ОБЕРНЕНИЙ ЗА МОДУЛЕМ)------------------------
print("Приклад 1:")
a = 3
m = 11
obratn_el = obratn(a, m)
if obratn_el is None:
    print(f"Оберненого елементу для {a} за модулем {m} не існує.")
else:
    print(f"Обернений елемент для {a} за модулем {m}: {obratn_el}")

##-------ПРИКЛАД 2 (ОБЕРНЕНИЙ ЗА МОДУЛЕМ)------------------------
print("\nПриклад 2:")
a = 10
m = 17
obratn_el = obratn(a, m)
if obratn_el is None:
    print(f"Оберненого елементу для {a} за модулем {m} не існує.")
else:
    print(f"Обернений елемент для {a} за модулем {m}: {obratn_el}")

##-------ПРИКЛАД 3 (ОБЕРНЕНИЙ ЗА МОДУЛЕМ)------------------------
print("\nПриклад 3:")
a = 6
m = 15
obratn_el = obratn(a, m)
if obratn_el is None:
    print(f"Оберненого елементу для {a} за модулем {m} не існує.")
else:
    print(f"Обернений елемент для {a} за модулем {m}: {obratn_el}")

#-------ПРИКЛАД 4 (ПОРІВНЯННЯ КІЛЬКА РОЗВ'ЯЗКІВ)------------------------
print("\nПриклад 4:")
a = 6
b = 18
m = 24
answers = congr(a, b, m)
if not answers:
    print(f"Для {a}x ≡ {b} (mod {m}) немає розв'язків.")
else:
    print(f"Розв'язки для {a}x ≡ {b} (mod {m}): {answers}")

#-------ПРИКЛАД 5 (ПОРІВНЯННЯ ЄДИНИЙ РОЗВ'ЯЗОК)------------------------
print("\nПриклад 5:")
a = 7
b = 5
m = 13
answers = congr(a, b, m)
if not answers:
    print(f"Для {a}x ≡ {b} (mod {m}) немає розв'язків.")
else:
    print(f"Розв'язок для {a}x ≡ {b} (mod {m}): {answers}")


#-------ПРИКЛАД 6 (ПОРІВНЯННЯ НЕМАЄ РОЗВ'ЯЗКІВ)------------------------
print("\nПриклад 6:")
a = 6
b = 5
m = 12
answers = congr(a, b, m)
if not answers:
    print(f"Для {a}x ≡ {b} (mod {m}) немає розв'язків.")
else:
    print(f"Розв'язок для {a}x ≡ {b} (mod {m}): {answers}")
