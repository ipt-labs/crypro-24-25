import random
import math

#----------------------------------------ПЕРШЕ ЗАВДАННЯ--------------------------------------
# Алгоритм Евкліда
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#Подільність Паскаля
def pascal(N, m, B=10):
    num_parts = []
    while N > 0:
        num_parts.append(N % B)
        N //= B

    r = [1]
    for i in range(1, len(num_parts)):
        r.append((r[i-1] * B) % m)
    
    lishok = sum(d * r[i] for i, d in enumerate(num_parts)) % m
    return lishok == 0

#Пробні ділення
def trial(N):
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23]    
    for prime in small:
        if pascal(N, prime):
            return False 
    return True 

#Міллер-Рабін
def miller_rabin(p, k=10):
    # Крок 0
    if p < 2 or p % 2 == 0:
        return p == 2 
    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1    
    # Крок 1
    def check(x):
        x = pow(x, d, p)
        if x == 1 or x == p - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                return False
        return True    
    # Крок 2
    counter = 0 
    for _ in range(k):
        x = random.randint(2, p - 2)
        
        if gcd(x, p) != 1:
            return False
        if check(x):
            return False
        counter += 1        
    # Крок 3
    if counter < k:
        return False
    return True

#Пошук на інтервалі
def find(start, finish):
    while True:
        number = random.randint(start, finish)
        if trial(number) and miller_rabin(number):
            return number

print("\033[36m" + "~~~" * 50 + "\033[0m")
start = int(input("Початок діапазона: ")) 
finish = int(input("Кінець діапазона: ")) 
simple=find(start, finish)
print("Випадкове просте число у заданому діапазоні: ", simple)

#----------------------------------------ДРУГЕ ЗАВДАННЯ--------------------------------------
def gen_pairs(bit_length=256):
    start = 2**(bit_length - 1)
    finish = 2**bit_length - 1
    
    p = find(start, finish)
    q = find(start, finish)
    p1 = find(start, finish)
    q1 = find(start, finish)
    
    while p * q > p1 * q1:
        p1 = find(start, finish)
        q1 = find(start, finish)
    
    """print("\033[36m" + "~~~" * 50 + "\033[0m")  
    print("Перша пара (абонент А):")
    print(f"p = {p}, q = {q}")
    print("\n")    
    print("\nДруга пара (абонент B):")
    print(f"p1 = {p1}, q1 = {q1}")"""
    return (p, q), (p1, q1)
#----------------------------------------ТРЕТЄ ЗАВДАННЯ--------------------------------------
#Розширений Евкліда
def gcd_evc(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = gcd_evc(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

#Обернений за модулем
def obratn(a, m):
    gcd, x, _ = gcd_evc(a, m)
    if gcd != 1:
        return None  
    return x % m 

#Функція Ойлера
def oiler(p, q):
    return (p - 1) * (q - 1)

#RSA
def rsa_pairs(bit_length=256):
    (p, q), _ = gen_pairs(bit_length=256)
    n = p * q
    phi = oiler(p, q)
    e = 2 ** 16 + 1
    if gcd(e, phi) != 1:
        raise ValueError("e повинно бути взаємнопростим з функцією Ойлера")
    d = obratn(e, phi) 
    return (d, p, q), (n, e)

keys_a = rsa_pairs()
keys_b = rsa_pairs()
secret_a, public_a = keys_a
secret_b, public_b = keys_b

print("\033[36m" + "~~~" * 50 + "\033[0m")
print("Абонент А:")
print(f"Секретний ключ: d = {secret_a[0]}")
print(f"Відкритий ключ: n = {public_a[0]}, e = {public_a[1]}")
print(f"p = {secret_a[1]}, q = {secret_a[2]}")
print("\n")
print("Абонент B:")
print(f"Секретний ключ: d1 = {secret_b[0]}")
print(f"Відкритий ключ: n1 = {public_b[0]}, e1 = {public_b[1]}")
print(f"p1 = {secret_b[1]}, q1 = {secret_b[2]}")

#----------------------------------------ЧЕТВЕРТЕ ЗАВДАННЯ--------------------------------------
def encrypt(message, public):
    n, e = public
    return pow(message, e, n)

def decrypt(cipher, secret):
    d, p, q = secret
    n = p*q
    return pow(cipher, d, n)

def sign(message, secret):
    d, p, q = secret
    n = p*q
    return pow(message, d, n)

def verify(message, sign, public):
    n, e = public
    return pow(sign, e, n) == message

from_a = random.randint(1000, 7000)
from_b = random.randint(1000, 7000)

print("\033[36m" + "~~~" * 50 + "\033[0m")
print('Повідомлення від А до B: ', from_a)
print('Зашифроване: ', encrypt(from_a, public_b))
print("\n")
print('Повідомлення від В до А: ', from_b)
print('Зашифроване: ', encrypt(from_b, public_a))

print("~~~" * 50)
print('Розшифрування повідомлення від В: ', decrypt(encrypt(from_b, public_a), secret_a))
print("\n")
print('Розшифрування повідомлення від А: ', decrypt(encrypt(from_a, public_b), secret_b))

sign_a = sign(from_a, secret_a)
sign_b = sign(from_b, secret_b)
print("~~~" * 50)
print('Підпис повідомлення від А: ', sign_a)
print("\n")
print('Підпис повідомлення від В: ', sign_b)

print("~~~" * 50)
print('Перевірка цифрового підпису для А: ', verify(from_a, sign_a, public_a))
print("\n")
print('Перевірка цифрового підпису для В: ', verify(from_b, sign_b, public_b))

#----------------------------------------П'ЯТЕ ЗАВДАННЯ--------------------------------------
def send_key(k, sender_se, sender_pub, receiver_pub):
    en_k = encrypt(k, receiver_pub)    
    signa = sign(k, sender_se)
    en_s = encrypt(signa, receiver_pub)   
    return en_k, en_s

def receive_key(en_key, en_signa, receiver_se, sender_pub):
    de_k = decrypt(en_key, receiver_se)    
    de_s = decrypt(en_signa, receiver_se)    
    valid_s = verify(de_k, de_s, sender_pub)    
    return de_k, valid_s

k = random.randint(1, public_b[1] - 1)
en_k, en_s = send_key(k, secret_a, public_a, public_b)
de_k, valid_s = receive_key(en_k, en_s, secret_b, public_a)

print("\033[36m" + "~~~" * 50 + "\033[0m")
print(f"А відправляє ключ: {k}\n")
print(f"Секретний ключ (A): d = {secret_a[0]}, p = {secret_a[1]}, q = {secret_a[2]}")
print(f"Відкритий ключ (A): n = {public_a[0]}, e = {public_a[1]}\n")
print("\n")
print(f"Зашифрований ключ: {en_k}\n")
print(f"Зашифрований підпис: {en_s}\n")
print("\n")
print("Абонент B отримує ключ:")
print(f"Секретний ключ (B): d = {secret_b[0]}, p = {secret_b[1]}, q = {secret_b[2]}")
print(f"Відкритий ключ (B): n = {public_b[0]}, e = {public_b[1]}\n")
print("\n")
print(f"Розшифрований ключ: {de_k}\n")
print(f"Чи вірний підпис?: {valid_s}")
