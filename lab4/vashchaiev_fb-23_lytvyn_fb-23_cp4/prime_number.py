import random

def get_s_d(d):
    d -= 1
    s = 0
    while(True):
        i, q = divmod(d, 2)
        if (q == 0):
            s += 1
            d = i
        else:
            return s, d

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def _pow(x, alpha, m):
    y = 1
    for bit in bin(alpha)[2:]:
        y = (y ** 2) % m
        if bit == '1':
            y = (y * x) % m
    return y


def rabin_subtest1(s, x, d, p):
    for r in range(1, 2 if s == 1 else s):
        x_r = _pow(x, d * (2 ** r), p)
        if x_r == p-1: # -1
            #print("* Сильно псевдопросте за основою x")
            return(x_r)
        elif x_r == 1:
            #print("НЕ є сильно псевдопросте за основою x")
            return(x_r)
    return 1
    

# True якщо просте
def rabin_test(p, k):
    counter = 0
    s, d = get_s_d(p)    
    while counter < k:
        x = random.randint(2, p)
        if (gcd(x, p) > 1):
            return False
        if (abs((_pow(x, d, p))) == 1):
            #print("1", "Сильно псевдопросте за основою x")
            counter += 1
            continue
        else:
            if rabin_subtest1(s, x, d, p) == 1:
                return False
            else:
                counter += 1
                continue
    return True

def get_p(a, b, k = 5):
    not_p = 0
    while(True):
        p = random.randrange(2 if a <= 1 else a, b)
        if (p%2 and p%3 and p%5 and p%7 and rabin_test(p, k)):
            print("failed attempts " + str(not_p))
            return p
        else:
            not_p += 1

if __name__ == "__main__":
    print(get_p(2 ** 256, 2 ** 512))

