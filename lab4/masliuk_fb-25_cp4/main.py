import random

def calculate_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_inverse_modulo(a, mod):
    t, new_t = 0, 1
    r, new_r = mod, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        return None
    if t < 0:
        t += mod
    return t


def miller_rabin_test(n):
    k = 100
    if n <= 1:
        return False
    if n <= 3:
        return True
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        x = random.randint(1, n)
        if calculate_gcd(n, x) != 1:
            return False
        xd = pow(x, d, n)
        if xd == 1 or xd == n - 1:
            return True
        for i in range(0, s - 1):
            w = (2**i)*d
            if pow(x, w, n) == n - 1:
                return True
    return False

def convert_decimal_to_hex(decimal_num):
    decimal_num = int(decimal_num)
    res = hex(decimal_num)
    return res[2:].upper()

def generate_random_prime_number(bits):
    while True:
        number = random.randint(2**(bits - 1), 2**bits - 1)
        if miller_rabin_test(number):
            return number

def generate_prime_pair(bits):
    p = generate_random_prime_number(bits)
    q = generate_random_prime_number(bits)
    p1 = generate_random_prime_number(bits)
    q1 = generate_random_prime_number(bits)

    if p*q > p1*q1:
        p, p1 = p1, p
        q, q1 = q1, q

    return p, q, p1, q1

def GenerateKeyPair(p, q):
    n = p*q
    f = (p-1)*(q-1)
    e = (2**16) + 1
    if calculate_gcd(e, f) != 1:
        return False
    else:
        m = find_inverse_modulo(e, f)
        if m < 0:
            d = m + f
        else:
            d = m
        public_k = (e, n)
        secret_k = (d, n)
        return public_k, secret_k

def Encrypt(key_p, M):
    e, n = key_p[0], key_p[1]
    C = pow(M, e, n)
    return C

def Decrypt(key_s, C):
    d, n = key_s[0], key_s[1]
    M = pow(C, d, n)
    return M

def Sign(key_s, k):
    d, n = key_s[0], key_s[1]
    S = pow(k, d, n)
    return S

def Verify(k, S, key_p):
    e, n = key_p[0], key_p[1]
    return k == pow(S, e, n)

def SendKey(key_s, key_p):
    e1, n1 = key_p[0], key_p[1]
    k = random.randint(1, 1000)
    k1 = pow(k, e1, n1)
    S = Sign(key_s, k)
    S1 = pow(S, e1, n1)
    return k1, S1, k

def ReceiveKey(key_s, k1, S1, key_p):
    d1, n1 = key_s[0], key_s[1]
    k = pow(k1, d1, n1)
    S = pow(S1, d1, n1)
    check = Verify(k, S, key_p)
    return check

print(miller_rabin_test(7))
print(miller_rabin_test(10))
print(generate_prime_pair(256))

a = generate_prime_pair(256)
for i in a:
    print(i)

Public_A, Secret_A = GenerateKeyPair(a[0], a[1])[0], GenerateKeyPair(a[0], a[1])[1]
Public_B, Secret_B = GenerateKeyPair(a[2], a[3])[0], GenerateKeyPair(a[2], a[3])[1]




print('Ключі A: ')
print('Public_A (e, n): ', Public_A, '\n', 'Secret_A (d, n): ', Secret_A)
print('')
print('Ключі B: ')
print('Public_B (e, n): ', Public_B, '\n', 'Secret_B (d, n): ', Secret_B, '\n \n')
print('Шифрування')
M_A = random.randint(0, 1000)
M_B = random.randint(0, 1000)
print('Повідомлення для B: ', '\n', M_B)
print('Зашифрований текст від A для B: ', '\n', Encrypt(Public_B, M_B), '\n')
print('Повідомлення для A: ', '\n', M_A)
print('Зашифрований текст від B для A: ', '\n', Encrypt(Public_A, M_A), '\n \n')
print('Розшифрування')
print('Розшифрований текст A від B: ', '\n', Decrypt(Secret_A, Encrypt(Public_A, M_A)))
print('Оригінальне повідомлення від B: ', '\n', M_A, '\n')
print('Розшифрований текст B від A: ', '\n', Decrypt(Secret_B, Encrypt(Public_B, M_B)))
print('Оригінальне повідомлення від A: ', '\n', M_B, '\n \n')
s1 = SendKey(Secret_A, Public_B)
k1 = s1[0]
S1 = s1[1]
print("Обмін ключами")
print('A генерує k1 та S1', '\n', 'k1: ', k1, '\n', 'S1: ', S1)
print('A надсилає повідомлення (k1, S1) до B. B отримав повідомлення')
print('B перевіряє підпис', '\n', 'Перевірено? ', ReceiveKey(Secret_B, k1, S1, Public_A), '\n \n')
s2 = SendKey(Secret_B, Public_A)
k2 = s2[0]
S2 = s2[1]
print('B генерує k2 та S2', '\n', 'k2: ', k2, '\n', 'S2: ', S2)
print('B надсилає повідомлення (k2, S2) до A. A отримав повідомлення')
print('A перевіряє підпис', '\n', 'Перевірено? ', ReceiveKey(Secret_A, k2, S2, Public_B), '\n \n')
e, n, d = Public_A[0], Public_A[1], Secret_A[0]
print('Перевірка через сервер')
print('\n Public_A: ')
print('e: ', convert_decimal_to_hex(e), '\n n: ', convert_decimal_to_hex(n))
print('\n Secret_A: ')
print('d: ', d)
e_server = int(str(input('Введіть експоненту сервера: ')), 16)
n_server = int(str(input('Введіть модуль сервера: ')), 16)
public_server = (e_server, n_server)

mess = int(str(input('Зашифроване повідомлення від сервера: ')), 16)
print('Розшифроване повідомлення A: ', convert_decimal_to_hex(Decrypt(Secret_A, mess)), '\n')

MM = random.randint(0, 1000)

print('Повідомлення для сервера: ', '\n', convert_decimal_to_hex(MM))
print('Зашифрований текст від А для сервера: ', '\n', convert_decimal_to_hex(Encrypt(public_server, MM)), '\n')

print('Використання функції перевірки')
serverk = int(str(input('Повідомлення від сервера: ')), 16)
serverS = int(str(input('Підпис від сервера: ')), 16)
print('Перевірка?', Verify(serverk, serverS, public_server), '\n')

print('Використання функції підпису')
k = random.randint(0, 1000)
SA = Sign(Secret_A, k)
print('k: ', convert_decimal_to_hex(k))
print('SA: ', convert_decimal_to_hex(SA))
print('Модуль: ', convert_decimal_to_hex(n))
print('Показник: ', convert_decimal_to_hex(e), '\n')

print('Сервер надсилає ключ, і ми намагаємося його перевірити')
k1s = int(str(input('k від сервера: ')), 16)
S1s = int(str(input('S від сервера: ')), 16)
print('А перевіряє підпис сервера', '\n', 'Чи було його перевірено? ', ReceiveKey(Secret_A, k1s, S1s, public_server), '\n')

print('Відправка ключа та S для сервера')

while Public_A[1] > public_server[1]:
    a = generate_prime_pair(256)
    Public_A, Secret_A = GenerateKeyPair(a[0], a[1])[0], GenerateKeyPair(a[0], a[1])[1]

print('Нові ключі А: ')
print('Public_A (e, n): ', '\n e: ', convert_decimal_to_hex(Public_A[0]), '\n n: ', convert_decimal_to_hex(Public_A[1]), '\n')

sA = SendKey(Secret_A, public_server)
k1A = sA[0]
S1A = sA[1]
kA = sA[2]
print('А генерує K1 і S1', '\n', 'K1: ', convert_decimal_to_hex(k1A), '\n', 'S1: ', convert_decimal_to_hex(S1A))
print('Модуль: ', convert_decimal_to_hex(Public_A[1]))
print('Показник: ', convert_decimal_to_hex(Public_A[0]))
print('Ключ (для перевірки): ', convert_decimal_to_hex(kA))
