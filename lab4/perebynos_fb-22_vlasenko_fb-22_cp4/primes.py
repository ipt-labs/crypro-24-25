from primality_tests import trial_division_test, miller_rabin_primality_test
from typing import Callable
from random import randint

k = 10
trial_divisions_count = 200

def _get_prime(bits_count: int, k: int, test_function: Callable[[int, int], bool]) -> int:
    n0 = 1 << (bits_count - 1)
    n1 = (1 << bits_count) - 1
    while True:
        x = randint(n0, n1)
        if x & 1 == 0:
            x += 1

        for i in range((n1 - x) >> 1):
            p = x + (i << 1)

            if not trial_division_test(p, trial_divisions_count):
                continue

            if test_function(p, k):
                return p

def get_prime(bits_count: int) -> int:
    return _get_prime(bits_count, k, miller_rabin_primality_test)

def _get_rsa_prime(bits_count: int, k: int, test_function: Callable[[int, int], bool]) -> int:
    while True:
        pp = _get_prime(bits_count-1, k, test_function)
        p = (pp << 1) + 1

        if not trial_division_test(p, trial_divisions_count):
            continue
    
        if test_function(p, k):
            return p

def get_rsa_prime(bits_count: int) -> int:
    return _get_rsa_prime(bits_count, k, miller_rabin_primality_test)
