import random
from sympy import mod_inverse

#Для виконання певнох частини коду їїї потрібно просто розкоментувати
#Для роботи із 10тковою системою числення потрібно усюди поприбирати функцію hex()
#===================Генерування ключів RSA===================

# def gcd(a, b):
#     while b:
#         a, b = b, a % b
#     return a

# def find_random_prime(start, end, k):
#     def is_prime(n):
#         if n <= 1:
#             return False
#         if n <= 3:
#             return True
#         # Пробні ділення на малі прості числа
#         small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
#         for prime in small_primes:
#             if n % prime == 0:
#                 return False

#         # Знаходимо d та s n-1 = d * 2^s
#         s = 0
#         d = n - 1
#         while d % 2 == 0:
#             d //= 2
#             s += 1

#         # Тест Міллера-Рабіна
#         def miller_rabin_test(a):
#             x = pow(a, d, n)
#             if x == 1 or x == n - 1:
#                 return True
#             for _ in range(s - 1):
#                 x = pow(x, 2, n)
#                 if x == n - 1:
#                     return True
#             return False

#         for _ in range(k):
#             a = random.randint(2, n - 2)
#             if not miller_rabin_test(a):
#                 return False
#         return True

#     while True:
#         candidate = random.randint(start, end)
#         if is_prime(candidate):
#             return candidate

# def generate_prime_pairs(bit_length=256):
#     start = 2**(bit_length - 1)
#     end = 2**bit_length - 1

#     # Генерація першої пари простих чисел p і q
#     p = find_random_prime(start, end, 5)
#     q = find_random_prime(start, end, 5)

#     # Генерація другої пари простих чисел p1 і q1
#     with open("invalid_pairs.txt", "w") as file:
#             while True:
#                 p1 = find_random_prime(start, end, 5)
#                 q1 = find_random_prime(start, end, 5)
#                 if p * q <= p1 * q1:
#                     break
#                 else:
#                     file.write(f"Пара ({p1}, {q1}) не підходить, оскільки {p} * {q} > {p1} * {q1}\n")
#     return (p, q), (p1, q1)

# def generate_rsa_keys_from_pairs(p, q):
#     # Обчислення n і φ(n)
#     n = p * q
#     phi_n = (p - 1) * (q - 1)
#     # Вибір відкритого експонента e
#     while True:
#         e = random.randint(3, phi_n - 1)
#         if gcd(e, phi_n) == 1:
#             break
#     # Обчислення секретного експонента d
#     d = mod_inverse(e, phi_n)
#     # Повернення відкритого і секретного ключів
#     public_key = (n, e)
#     private_key = (d, p, q)
#     return public_key, private_key

#===================Шифрування та розшифрування RSA===================
def encrypt(message, public_key):
    n, e = public_key
    return pow(message, e, n)

def decrypt(cipher, private_key):
    d, p, q = private_key
    n = p * q 
    message = pow(cipher, d, n)
    return message

def sign(message, private_key):
    d, p, q = private_key
    n = p * q  
    signature = pow(message, d, n)
    return signature

def verify(message, signature, public_key):
    n, e = public_key
    verified_message = pow(signature, e, n)
    return verified_message == message

def send_key(key, sender_private_key, receiver_public_key):
    # Підписання ключа відправником
    signature = sign(key, sender_private_key)
    # Шифрування ключа для отримувача
    encrypted_key = encrypt(key, receiver_public_key)
    return encrypted_key, signature

def receive_key(encrypted_key, signature, sender_public_key, receiver_private_key):
    # Розшифрування ключа отримувачем
    key = decrypt(encrypted_key, receiver_private_key)
    # Перевірка підпису відправника
    if verify(key, signature, sender_public_key):
        return key
    else:
        raise ValueError("Підпис недійсний!")

def main():
    #Генерація двох пар простих чисел
    # (p, q), (p1, q1) = generate_prime_pairs()

    #Генерація ключових пар для абонентів А і B
    # public_key_A, private_key_A = generate_rsa_keys_from_pairs(p, q)
    # public_key_B, private_key_B = generate_rsa_keys_from_pairs(p1, q1)

    # print(f"Відкритий ключ абонента А: (e, n) = ({public_key_A[1]}, {public_key_A[0]})")
    # print(f"Секретний ключ абонента А: (d, p, q) = ({private_key_A[0]}, {private_key_A[1]}, {private_key_A[2]})")
    # print(f"Відкритий ключ абонента B: (e, n) = ({public_key_B[1]}, {public_key_B[0]})")
    # print(f"Секретний ключ абонента B: (d, p, q) = ({private_key_B[0]}, {private_key_B[1]}, {private_key_B[2]})")

    # #Згенеровані значення абонентів А та В
    # public_key_A = (8573503295857509923938416470442077851388989055726637479266345560549570425255737807589105165498414015801671773830005434289019936108143251035039524653325583, 2238525690251961136637344078371838105438432066378209107894448446397125586554647135874581643541963499364765832154106216127990103619928312731173141893554123)
    # private_key_A = (2502632654446164099471923137609512597795768901033766674775644255218756295380474184452057702819798732651554522715183212475698547402555389608021596769551347, 111037008699443494319846787257631372789995452751970566491626186746427276878843, 77213024704802583634157729708137941185979461185084197953657676385895076285181)
    # public_key_B = (9351834343321630959261376981888548165616839462176426375700965248436843864846565111143800948464728532125013352369202171373730492204998536960456782395737383 ,27523579304756039532527119828668349646059390570892115279669929033569241565499736288074646886462276998847907609444529923298457360398023235254324122092917)
    # private_key_B = (7996502677137744306466114291265103163224697003766021296217175731007477983614990252508400776109079741991747013971958352728415342880259972152597065642762981, 111224351447191284199010921433359767377223566654084985981081557289664235478837, 84080817030089233023024835269383448526219000866175631491814728840915823678059)
    

    # # Вибір відкритого повідомлення M
    # M = random.randint(1, min(public_key_A[0], public_key_B[0]) - 1)
    # M = 103417908096753293107748111040875722128999286030092950873465642585967  # Вибране повідомлення
    # print(f"Відкрите повідомлення M: {hex(M)}")

    # # # Шифрування та розшифрування повідомлення
    # cipher_A = encrypt(M, public_key_A)
    # print(f"Криптограма для абонента А: {cipher_A}")
    # l_A = decrypt(cipher_A, private_key_A)
    # print(f"Розшифроване повідомлення абонента А: {l_A}")
    # cipher_B = encrypt(M, public_key_B)
    # print(f"Криптограма для абонента А: {cipher_B}")
    # l_B = decrypt(cipher_B, private_key_B)
    # print(f"Розшифроване повідомлення абонента B: {l_B}")
    # if l_A == M and l_B == M:
    #     print("Повідомлення розшифровані вірно")
    # else:
    #     print("Повідомлення розшифровані невірно")

    # # Підпис та перевірка повідомлення
    # signature_A = sign(M, private_key_A) #Цей же підпис і для взаємодії із сервером
    # print(f"Підпис абонента А: {hex(signature_A)}") #Тільки перед підписом треба додати hex()
    # # verified_message_A = verify(M, signature_A, public_key_A)
    # print(f"Перевірене повідомлення абонента А: {verified_message_A}")
    # signature_B = sign(M, private_key_B)
    # print(f"Підпис абонента B: {signature_B}")
    # verified_message_B = verify(M, signature_B, public_key_B)
    # print(f"Перевірене повідомлення абонента B: {verified_message_B}")

    # Вибір випадкового ключа k
    # k = random.randint(1, min(public_key_A[0], public_key_serv[0]) - 1)
    # print(f"Випадковий ключ k: {hex(k)}")

    # # Відправник (А) відправляє ключ k отримувачу (B)
    # encrypted_key, signature = send_key(k, private_key_A, public_key_B)
    # print(f"Зашифрований ключ: {encrypted_key}")
    # print(f"Підпис: {signature}")

    # # Отримувач (B) отримує ключ k від відправника (А)
    # received_key = receive_key(encrypted_key, signature, public_key_A, private_key_B)
    # print(f"Отриманий ключ: {received_key}")

    # # Перевірка правильності отриманого ключа
    # assert k == received_key, "Отриманий ключ невірний!"
    # print("Отриманий ключ правильний.")

    # # Перевірка взаємодією із тестовим середовищем Asym Crypto Lab Environment
    # public_key_serv = (60059724760081170307872390905278238563065865687640799498300153216416031436007, 65537)
    
    # public_key_A = (8573503295857509923938416470442077851388989055726637479266345560549570425255737807589105165498414015801671773830005434289019936108143251035039524653325583, 2238525690251961136637344078371838105438432066378209107894448446397125586554647135874581643541963499364765832154106216127990103619928312731173141893554123)
    # n = public_key_A[0]
    # e = public_key_A[1]
    # print(f"Відкритий ключ абонента А: (e, n) = ({hex(e)}, {hex(n)})") # Переводимо у хексадецимальну систему числення
    # # Шифрування
    # cipher_A = encrypt(M, public_key_A) #Шифруємо ключем абонента А
    # print(f"Криптограма для абонента А: {hex(cipher_A)}")

    # cipher_serv = encrypt(M, public_key_serv) #Шифруємо ключем серверу
    # print(f"Криптограма для серверу: {hex(cipher_serv)}")
    # signature_serv = 0x0A1BF7D0A0C35103B5EA1E0478106252A3F942178DC571CD6C0142DDFB675AB2
    # verified_message_serv = verify(M, signature_serv, public_key_serv) #Перевіряємо повідомлення підписом сервера
    # print(f"Перевірене повідомлення серверу: {verified_message_serv}")

    # # Відправник (А) відправляє ключ k отримувачу (serv) - шось пішло не так
    # encrypted_key, signature = send_key(k, private_key_A, public_key_serv)
    # print(f"Зашифрований ключ: {hex(encrypted_key)}")
    # print(f"Підпис: {hex(signature)}")   




if __name__ == "__main__":
    main()