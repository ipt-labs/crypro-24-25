from argparse import ArgumentParser
from random import randint
from math import gcd


def find_rand_int(max_len, min_len=256):
    if max_len < min_len:
        return 1
    
    while True:
        p = randint(2**min_len, 2**max_len)
        k, d, s = 30, p-1, 0

        while d % 2 == 0:
            d = d // 2
            s += 1

        simple = True
        for _ in range(k):
            x = randint(2, p)
            if gcd(x, p) > 1:
                simple = False
                break
            
            if pow(x, d, p) in {1, p-1}:
                continue
            
            for r in range(1, s):
                if pow(x, d * (2**r), p) == p-1:
                    break
            else:
                simple = False
                      
        if simple == False:
            continue
        return p


def pq_and_p1q1_create(max_len):
    a = []
    for _ in range(4):
        a.append(find_rand_int(max_len))
    a.sort()
    return a[0], a[1], a[2], a[3]


class RSA:
    def __init__(self, p_, q_):
        self.p_ = p_
        self.q_ = q_
        self.public_key, self.private_key = self.find_rsa()

    def find_rsa(self):
        n = self.q_ * self.p_
        On = (self.q_ - 1)*(self.p_ - 1)

        while True:
            e = randint(2, On - 1)
            if gcd(e, On) == 1:
                break
        d = pow(e, -1, On)
        return (n, e), (d, self.p_, self.q_)

    def encrypt(self, msg, reciver_public_key):
        return pow(msg, reciver_public_key[1], reciver_public_key[0])

    def decrypt(self, msg, reciver_secret_key):
        return pow(msg, reciver_secret_key[0], reciver_secret_key[1] * reciver_secret_key[2])

    def sign(self, msg, sender_secret_key):
        return (pow(msg, sender_secret_key[0], sender_secret_key[1] * sender_secret_key[2]), msg)

    def verify(self, msg, sender_public_key):
        return msg[1] == pow(msg[0], sender_public_key[1], sender_public_key[0])


class A_abonent(RSA):
    def sendkey(self, reciver_public_key):
        k = randint(0, self.private_key[1] * self.private_key[2])
        s = self.sign(k, self.private_key)
        s1 = self.encrypt(s[0], reciver_public_key)
        k1 = self.encrypt(k, reciver_public_key)
        return k1, s1


class B_abonent(RSA):
    def receivekey(self, msg, sender_public_key):
        k = self.decrypt(msg[0], self.private_key)
        s = self.decrypt(msg[1], self.private_key)
        if self.verify((s, k), sender_public_key):
            print('Успішний обмін ключами')
        else:
            raise ValueError('Невдалий обмін')


def init():
    arg_pars = ArgumentParser(
        prog='Лабораторна робота №4, зробили студенти групи ФБ-22 Швайка та Філонов',
    )
    arg_pars.add_argument('MAX')
    arg_pars.add_argument('MSG')
    args = arg_pars.parse_args()

    val = find_rand_int(int(args.MAX))
    pairs = pq_and_p1q1_create(int(args.MAX))

    a_abonent = A_abonent(pairs[0], pairs[1])
    b_abonent = B_abonent(pairs[2], pairs[3])

    print(f'''
    Випадкове просте число:
     {val}

    Значення пар pq (для абонента А) та p1q1 (для абонента В)
     1)p: {pairs[0]}
       q: {pairs[1]}
       
     2)p1:{pairs[2]}
       q1:{pairs[3]}
        
    RSA:
     1)A: 
        SECRET key
        d: {hex(int(a_abonent.private_key[0]))}
        
        PUBLIC key
        n: {hex(int(a_abonent.public_key[0]))}
        e: {hex(int(a_abonent.public_key[1]))}

     2)B: 
        SECRET key
        d: {hex(int(b_abonent.private_key[0]))}

        PUBLIC key
        n: {hex(int(b_abonent.public_key[0]))}
        e: {hex(int(b_abonent.public_key[1]))} 
    ''')

    print('\nОбмін ключами між абонентами А та В')
    try:
        k1, s1 = a_abonent.sendkey(b_abonent.public_key)  
        b_abonent.receivekey((k1, s1), a_abonent.public_key) 

        print(f'''
        Початок обміну повідомленнями між абонентами А та В
        Вихідне повідомлення (A): 
            {hex(int(args.MSG))}
        ''')

        enc_msg = a_abonent.encrypt((int(args.MSG)), b_abonent.public_key)
        print(f'''
        Зашифроване повідомлення (A -> B): 
            {hex(int(enc_msg))}
        ''')

        dec_msg = b_abonent.decrypt(enc_msg, b_abonent.private_key)
        print(f'Розшифроване повідомлення (B): {hex(int(dec_msg))}')        
    except:
        print('Невдалий обмін')
        return

init()
