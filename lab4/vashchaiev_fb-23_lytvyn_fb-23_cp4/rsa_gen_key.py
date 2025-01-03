import random
import json
import prime_number as pn

json_obj = list()

def get_e(fn):
    while True:
        e = random.randint(2, fn)
        if (pn.gcd(e, fn) == 1):
            return e

def mod_invert(a, m):
    a = a % m
    if a == 0:
        return None

    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0

    return x1 + m0 if x1 < 0 else x1

class Keys:
    def __init__(self, d, p, q, n, e):
        self.d = d
        self.p = p
        self.q = q
        self.n = n
        self.e = e

# a, b діапазон довжини p, q в бітах
def GenerateKeyPair(a, b):
    min = 2 ** a
    max = 2 ** b
    p = pn.get_p(min, max)
    q = pn.get_p(min, max)
    n = p*q
    fn = (p-1)*(q-1)
    e = get_e(fn)
    d = mod_invert(e, fn) % fn
    return Keys(d=d, p=p, q=q, n=n, e=e)

if __name__ == "__main__":
    # При цьому пари чисел беруться так, щоб p * q <= p1 * q1
    while True:
        alice = GenerateKeyPair(256, 512)
        bob = GenerateKeyPair(256, 512)
        if alice.p * alice.q <= bob.p * bob.q:
            break

    json_obj.append({"name": "Alice", "my_keys": {"d": hex(alice.d)[2:], "p": hex(alice.p)[2:], "q": hex(alice.q)[2:], "n": hex(alice.n)[2:], "e": hex(alice.e)[2:]}, "open_for_me": {"n": hex(bob.n)[2:], "e": hex(bob.e)[2:]}})
    json_obj.append({"name": "Bob", "my_keys": {"d": hex(bob.d)[2:], "p": hex(bob.p)[2:], "q": hex(bob.q)[2:], "n": hex(bob.n)[2:], "e": hex(bob.e)[2:]}, "open_for_me": {"n": hex(alice.n)[2:], "e": hex(alice.e)[2:]}})

    with open("keys.json", "w") as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=4)
    
    print("Alice")
    print("p", len(bin(alice.p)[2:]), "bits", hex(alice.p)[2:])
    print("q", len(bin(alice.q)[2:]), "bits", hex(alice.q)[2:])

    print("Bob")
    print("p1", len(bin(bob.p)[2:]), "bits", hex(bob.p)[2:])
    print("q1", len(bin(bob.q)[2:]), "bits", hex(bob.q)[2:])