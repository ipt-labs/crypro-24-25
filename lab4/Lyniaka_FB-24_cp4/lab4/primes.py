from random import randint

from bigram_affine_cipher import gcd


PRIME_TESTS_QUANTITY = 10


def swift_power(x, a, m):
    """x**a (mod m)"""
    ai_list = list()
    while a > 0:
        ai_list.append(a % 2)
        a //= 2
    y = 1
    for i in range(len(ai_list) - 1, -1, -1):
        y = (y ** 2) % m
        y = y if ai_list[i] == 0 else (y * x) % m
    return y


def miller_rabin_primes_test(p, k):
    if p % 2 == 0:
        return False

    d = (p - 1) // 2
    s = 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for i in range(k):
        # print("i=", i)
        a = randint(1, p)
        if gcd(a, p) > 1:
            return False
        # print("a=", a, "d=", d)
        # u = (a ** d) % p
        u = swift_power(a, d, p)
        # print(u)
        if u != 1:
            j = 1
            while u != p - 1 and j < s:
                u = (u ** 2) % p
                j += 1
                # print("j=", j)
            if u != p - 1:
                return False
    return True


def select_prime(n0, n1):
    """select prime p: n0 <= p <= n1"""
    x = randint(n0, n1)
    m0 = x if x % 2 != 0 else x + 1
    for i in range((n1 - m0) // 2):
        p = m0 + 2 * i
        if miller_rabin_primes_test(p, PRIME_TESTS_QUANTITY):
            return p

    return None


def select_prime_multiplied(pp):
    """select prime p = 2ipp + 1"""
    result = None
    i = 0
    while True:
        i += 1
        p = 2 * i * pp + 1
        if miller_rabin_primes_test(p, PRIME_TESTS_QUANTITY):
            result = p
            break

    return result


def select_prime_with_prime_divisor(n0, n1):
    """select primes p', p: p = 2ip' + 1"""
    n02 = n0 // 2
    n12 = n1 // 2
    while True:
        pp = select_prime(n02, n12)
        if pp:
            break

    p = select_prime_multiplied(pp)
    return p


def select_primes_pair(n0, n1):
    p = select_prime_with_prime_divisor(n0, n1)
    q = select_prime_with_prime_divisor(n0, n1)
    return p, q


def select_two_primes_pairs(n0, n1):
    p, q = select_primes_pair(n0, n1)
    p1, q1 = select_primes_pair(n0, n1)
    if p * q > p1 * q1:
        p, p1 = p1, p
        q, q1 = q1, q
    return p, q, p1, q1


def oyler_phi(p, q):
    return (p -1) * (q - 1)


if __name__ == "__main__":
    print(miller_rabin_primes_test(93, 10))
    print(miller_rabin_primes_test(103, 10))
    print(miller_rabin_primes_test(2 ** 256 - 1, 10))
    p, q, p1, q1 = select_two_primes_pairs(2 ** 256, 2 ** 257)
    print(p, q)
    print(p1, q1)
