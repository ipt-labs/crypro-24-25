from helpers import gcd_extended_euclid, horner_pow_2, jacobi_symbol_2
from random import randint

first_200_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                    179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                    283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                    419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
                    547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
                    661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
                    811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
                    947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
                    1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223]

# gcd(a, p) = 1 and a^(p-1) = 1 mod p
def check_pseudo_prime(base: int, p: int) -> bool:
    return gcd_extended_euclid(base, p)[0] == 1 and horner_pow_2(base, p-1, p) == 1

# gcd(a, p) = 1 and a^((p-1)/2) = jacobi(a, p) mod p
def check_pseudo_prime_jacobi_euler(base: int, p: int) -> bool:
    return gcd_extended_euclid(base, p)[0] == 1 and (jacobi_symbol_2(base, p) % p) == horner_pow_2(base, (p-1) >> 1, p)

def split_by_2(n: int) -> tuple[int]:
    d = n - 1
    s = 0
    while d & 1 == 0:
        s += 1
        d >>= 1

    return s, d

def _check_pseudo_prime_strong(base: int, p: int, s: int, d: int) -> bool:
    if horner_pow_2(base, d, p) == 1:
        return True

    s -= 1
    while s >= 0:
        if horner_pow_2(base, d << s, p) == p - 1:
            return True
        s -= 1

    return False

# p - 1 = 2^s * d and (a^d = 1 mod p or a^(2^r * d) = -1 mod p for some r in [0, s-1]) 
def check_pseudo_prime_strong(base: int, p: int) -> bool:
    s, d = split_by_2(p)
    return _check_pseudo_prime_strong(base, p, s, d)

def trial_division_test(p: int, probes: int) -> bool:
    # skip this because can't take sqrt of very big numbers
    # probes = min(int(sqrt(p)) // 2, probes)
    for i in first_200_primes[:probes]:
        if p % i == 0:
            return False

    return True

def fermat_primality_test(p: int, k: int) -> bool:
    for _ in range(k):
        x = randint(2, p-1)
        if gcd_extended_euclid(x, p)[0] != 1:
            return False
        
        if not check_pseudo_prime(x, p):
            return False
    
    return True

def solovay_strassen_primality_test(p: int, k: int) -> bool:
    for _ in range(k):
        x = randint(2, p-1)
        if gcd_extended_euclid(x, p)[0] != 1:
            return False
        
        if not check_pseudo_prime_jacobi_euler(x, p):
            return False
    
    return True

def miller_rabin_primality_test(p: int, k: int) -> bool:
    s, d = split_by_2(p)
    for _ in range(k):
        x = randint(2, p-1)
        if gcd_extended_euclid(x, p)[0] != 1:
            return False
        
        if not _check_pseudo_prime_strong(x, p, s, d):
            return False

    return True


def main():
    # check_pseudo_prime tests
    # Primes should return True
    assert check_pseudo_prime(2, 3) == True
    assert check_pseudo_prime(2, 5) == True
    assert check_pseudo_prime(2, 7) == True
    assert check_pseudo_prime(2, 11) == True
    assert check_pseudo_prime(2, 13) == True
    assert check_pseudo_prime(2, 17) == True
    assert check_pseudo_prime(2, 19) == True
    assert check_pseudo_prime(2, 23) == True
    assert check_pseudo_prime(2, 29) == True
    assert check_pseudo_prime(2, 31) == True

    # Composites should return False unless pseudoprime to base
    assert check_pseudo_prime(2, 4) == False
    assert check_pseudo_prime(2, 6) == False
    assert check_pseudo_prime(2, 9) == False
    assert check_pseudo_prime(2, 15) == False
    assert check_pseudo_prime(2, 21) == False

    # Pseudoprimes to base 2
    assert check_pseudo_prime(2, 341) == True   # 341 is pseudoprime to base 2
    assert check_pseudo_prime(2, 561) == True   # 561 is pseudoprime to base 2
    assert check_pseudo_prime(2, 645) == True   # 645 is pseudoprime to base 2
    assert check_pseudo_prime(2, 1105) == True  # 1105 is pseudoprime to base 2
    assert check_pseudo_prime(2, 1729) == True  # 1729 is pseudoprime to base 2

    # Other bases
    assert check_pseudo_prime(3, 91) == True   # 91 is prime
    assert check_pseudo_prime(3, 121) == True  # 121 is composite and pseudoprime to base 3
    assert check_pseudo_prime(3, 561) == False   # 561 is not pseudoprime to base 3
    assert check_pseudo_prime(5, 91) == False   # 91 is composite, not pseudoprime to base 5
    assert check_pseudo_prime(5, 561) == True   # 561 is pseudoprime to base 5
    print("check_pseudo_prime tests passed")

    # check_pseudo_prime_jacobi_euler tests
    # Primes should return True
    assert check_pseudo_prime_jacobi_euler(2, 3) == True
    assert check_pseudo_prime_jacobi_euler(2, 5) == True
    assert check_pseudo_prime_jacobi_euler(2, 7) == True
    assert check_pseudo_prime_jacobi_euler(2, 11) == True
    assert check_pseudo_prime_jacobi_euler(2, 13) == True
    assert check_pseudo_prime_jacobi_euler(2, 17) == True
    assert check_pseudo_prime_jacobi_euler(2, 19) == True
    assert check_pseudo_prime_jacobi_euler(2, 23) == True
    assert check_pseudo_prime_jacobi_euler(2, 29) == True
    assert check_pseudo_prime_jacobi_euler(2, 31) == True

    # Composites should return False
    assert check_pseudo_prime_jacobi_euler(2, 4) == False
    assert check_pseudo_prime_jacobi_euler(2, 6) == False
    assert check_pseudo_prime_jacobi_euler(2, 9) == False
    assert check_pseudo_prime_jacobi_euler(2, 15) == False
    assert check_pseudo_prime_jacobi_euler(2, 21) == False

    # Euler pseudoprimes to base 2
    assert check_pseudo_prime_jacobi_euler(2, 341) == False     # 341 not Euler-Jacobi pseudoprime to base 2
    assert check_pseudo_prime_jacobi_euler(2, 561) == True      # 561 Euler-Jacobi pseudoprime to base 2
    assert check_pseudo_prime_jacobi_euler(2, 645) == False

    # Other bases
    assert check_pseudo_prime_jacobi_euler(3, 91) == False
    assert check_pseudo_prime_jacobi_euler(3, 121) == True
    assert check_pseudo_prime_jacobi_euler(5, 91) == False
    assert check_pseudo_prime_jacobi_euler(5, 121) == False
    assert check_pseudo_prime_jacobi_euler(5, 781) == True

    # Large primes
    assert check_pseudo_prime_jacobi_euler(2, 104729) == True  # 10000th prime
    assert check_pseudo_prime_jacobi_euler(3, 104729) == True
    print("check_pseudo_prime_jacobi_euler tests passed")

    # check_pseudo_prime_strong tests
    # Primes should return True
    assert check_pseudo_prime_strong(2, 3) == True
    assert check_pseudo_prime_strong(2, 5) == True
    assert check_pseudo_prime_strong(2, 7) == True
    assert check_pseudo_prime_strong(2, 11) == True
    assert check_pseudo_prime_strong(2, 13) == True
    assert check_pseudo_prime_strong(2, 17) == True
    assert check_pseudo_prime_strong(2, 19) == True
    assert check_pseudo_prime_strong(2, 23) == True
    assert check_pseudo_prime_strong(2, 29) == True
    assert check_pseudo_prime_strong(2, 31) == True

    # Composites should return False
    assert check_pseudo_prime_strong(2, 4) == False
    assert check_pseudo_prime_strong(2, 6) == False
    assert check_pseudo_prime_strong(2, 9) == False
    assert check_pseudo_prime_strong(2, 15) == False
    assert check_pseudo_prime_strong(2, 21) == False

    # Strong pseudoprimes to base 2
    assert check_pseudo_prime_strong(2, 2047) == True   # 2047 = 23 * 89
    assert check_pseudo_prime_strong(2, 3277) == True   # 3277 = 29 * 113
    assert check_pseudo_prime_strong(2, 4033) == True   # 4033 = 37 * 109
    assert check_pseudo_prime_strong(2, 4681) == True   # 4681 = 43 * 109
    assert check_pseudo_prime_strong(2, 8321) == True   # 8321 = 53 * 157

    # Carmichael numbers are pseudoprimes but not strong pseudoprimes to base 2
    assert check_pseudo_prime_strong(2, 561) == False   # 561 = 3 * 11 * 17

    # Other bases
    assert check_pseudo_prime_strong(3, 91) == False    # 91 = 7 * 13
    assert check_pseudo_prime_strong(3, 121) == True   # 121 = 11 * 11
    assert check_pseudo_prime_strong(3, 561) == False
    assert check_pseudo_prime_strong(5, 1105) == False  # 1105 = 5 * 13 * 17
    assert check_pseudo_prime_strong(5, 5611) == True  

    # Large primes
    assert check_pseudo_prime_strong(2, 104729) == True  # 10000th prime
    assert check_pseudo_prime_strong(3, 104729) == True
    print("check_pseudo_prime_strong tests passed")
    print("All tests passed.")

if __name__ == "__main__":
    main()
