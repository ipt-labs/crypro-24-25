import time

from functools import wraps

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


# It looks fast enough
def gcd_extended_euclid(a: int, m: int) -> tuple[int]:
    """
    u(0) = 1, u(1) = 0, u(i+1) = u(i-1) - q(i) * u(i);
    """
    modulo = m
    a, m = abs(a), abs(m)
    if a == 0:
        return m, 0
    if m == 0:
        return a, 0
    
    u0, u1 = 1, 0
    while m:
        u0, u1 = u1, u0 - (a // m) * u1
        a, m = m, a % m

    return a, u0 % modulo


# I think this is the fastest thing you 
# can do with Horner's scheme in python.
def horner_pow(x: int, a: int, m: int) -> int:
    k = a.bit_length()
    y = 1
    for i in range(k-1, -1, -1):
        y = (y * y) % m
        y = (y * (x if (a >> i) & 1 else 1)) % m
    
    return y


# It is even faster than the previous one, 
# probably because there is no method call 
# and no need to create a range for iteration. 
def horner_pow_2(x: int, a: int, m: int) -> int:
    y = 1
    while a:
        if a & 1:
            y = (y * x) % m
        x = (x * x) % m
        a >>= 1
    
    return y


def jacobi_symbol(a: int, n: int) -> int:
    # n odd, greater than 1
    if not n > 1 or n % 2 == 0:
        return 0
    
    a %= n

    if gcd_extended_euclid(a, n)[0] != 1:
        return 0

    # (1/n) = 1
    if a == 1:
        return 1

    twos = 0
    while a & 1 == 0:
        twos ^= 1
        a >>= 1

    twos = -1 if ((n**2-1) // 8) % 2 == 1 and twos != 0 else 1

    if a == 1:
        return twos
    
    return jacobi_symbol(n, a) * (-1 if ((a-1) // 2) % 2 == 1 and ((n-1) // 2) % 2 == 1 else 1) * twos


# https://en.wikipedia.org/wiki/Jacobi_symbol#Implementation_in_C++
def jacobi_symbol_2(a: int, n: int) -> int:
    if not n > 1 or n & 1 == 0:
        raise ValueError(f"n={n} must be odd and greater than 1")
    
    a %= n
    # XOR of bits 1 and 2 determines sign of return value
    t = 0
    while a != 0:
        while a & 0b11 == 0:
            a >>= 2
        if a & 1 == 0:
            # Could be "^= n & 6"; we only care about bits 1 and 2
            t ^= n
            a >>= 1
        
        # Flip sign if a % 4 == n % 4 == 3
        t ^= a & n & 2
        r = n % a
        n = a
        a = r
    
    if n != 1:
        return 0
    elif (t ^ (t >> 1)) & 2:
        return -1
    else:
        return 1


def main():
    # jacobi symbol tests
    assert jacobi_symbol(13, 187) == -1
    assert jacobi_symbol(2, 3) == -1
    assert jacobi_symbol(3, 5) == -1
    assert jacobi_symbol(5, 11) == 1
    assert jacobi_symbol(10, 21) == -1
    assert jacobi_symbol(7, 15) == -1
    assert jacobi_symbol(9, 19) == 1
    assert jacobi_symbol(8, 23) == 1
    assert jacobi_symbol(12, 25) == 1
    assert jacobi_symbol(14, 27) == -1
    assert jacobi_symbol(15, 29) == -1
    assert jacobi_symbol(16, 31) == 1
    assert jacobi_symbol(18, 33) == 0
    assert jacobi_symbol(20, 35) == 0
    assert jacobi_symbol(21, 37) == 1
    assert jacobi_symbol(22, 39) == 1
    assert jacobi_symbol(24, 41) == -1
    assert jacobi_symbol(25, 43) == 1
    assert jacobi_symbol(26, 45) == 1
    assert jacobi_symbol(28, 47) == 1
    print("All jacobi symbol tests passed.")

    # jacobi symbol tests
    assert jacobi_symbol_2(13, 187) == -1
    assert jacobi_symbol_2(2, 3) == -1
    assert jacobi_symbol_2(3, 5) == -1
    assert jacobi_symbol_2(5, 11) == 1
    assert jacobi_symbol_2(10, 21) == -1
    assert jacobi_symbol_2(7, 15) == -1
    assert jacobi_symbol_2(9, 19) == 1
    assert jacobi_symbol_2(8, 23) == 1
    assert jacobi_symbol_2(12, 25) == 1
    assert jacobi_symbol_2(14, 27) == -1
    assert jacobi_symbol_2(15, 29) == -1
    assert jacobi_symbol_2(16, 31) == 1
    assert jacobi_symbol_2(18, 33) == 0
    assert jacobi_symbol_2(20, 35) == 0
    assert jacobi_symbol_2(21, 37) == 1
    assert jacobi_symbol_2(22, 39) == 1
    assert jacobi_symbol_2(24, 41) == -1
    assert jacobi_symbol_2(25, 43) == 1
    assert jacobi_symbol_2(26, 45) == 1
    assert jacobi_symbol_2(28, 47) == 1
    print("All jacobi symbol 2 tests passed.")

    # horner pow tests
    assert horner_pow(2, 3, 5) == 3
    assert horner_pow(3, 4, 7) == 4
    assert horner_pow(5, 6, 11) == 5
    assert horner_pow(7, 8, 13) == 3
    assert horner_pow(9, 10, 17) == 13
    assert horner_pow(11, 12, 19) == 1
    assert horner_pow(13, 14, 23) == 12
    assert horner_pow(15, 16, 29) == 7
    assert horner_pow(17, 18, 31) == 16
    assert horner_pow(19, 20, 37) == 9
    assert horner_pow(21, 22, 41) == 31
    assert horner_pow(23, 24, 43) == 41
    assert horner_pow(25, 26, 47) == 21
    assert horner_pow(27, 28, 53) == 13
    assert horner_pow(29, 30, 59) == 29
    assert horner_pow(31, 32, 61) == 15
    assert horner_pow(33, 34, 67) == 33
    assert horner_pow(35, 36, 71) == 36
    assert horner_pow(37, 38, 73) == 55
    assert horner_pow(39, 40, 79) == 40
    print("All horner pow tests passed.")

    # horner pow tests
    assert horner_pow_2(2, 3, 5) == 3
    assert horner_pow_2(3, 4, 7) == 4
    assert horner_pow_2(5, 6, 11) == 5
    assert horner_pow_2(7, 8, 13) == 3
    assert horner_pow_2(9, 10, 17) == 13
    assert horner_pow_2(11, 12, 19) == 1
    assert horner_pow_2(13, 14, 23) == 12
    assert horner_pow_2(15, 16, 29) == 7
    assert horner_pow_2(17, 18, 31) == 16
    assert horner_pow_2(19, 20, 37) == 9
    assert horner_pow_2(21, 22, 41) == 31
    assert horner_pow_2(23, 24, 43) == 41
    assert horner_pow_2(25, 26, 47) == 21
    assert horner_pow_2(27, 28, 53) == 13
    assert horner_pow_2(29, 30, 59) == 29
    assert horner_pow_2(31, 32, 61) == 15
    assert horner_pow_2(33, 34, 67) == 33
    assert horner_pow_2(35, 36, 71) == 36
    assert horner_pow_2(37, 38, 73) == 55
    assert horner_pow_2(39, 40, 79) == 40
    print("All horner pow 2 tests passed.")

    # Find reverse element in Zm
    assert gcd_extended_euclid(0, 0) == (0, 0)
    assert gcd_extended_euclid(0, 1) == (1, 0)
    assert gcd_extended_euclid(1, 0) == (1, 0)
    assert gcd_extended_euclid(1, 1) == (1, 0)
    assert gcd_extended_euclid(2, 3) == (1, 2)
    assert gcd_extended_euclid(2, 5) == (1, 3)
    assert gcd_extended_euclid(5, 11) == (1, 9)
    assert gcd_extended_euclid(3, 20) == (1, 7)
    assert gcd_extended_euclid(9, 13) == (1, 3)
    print("All gcd extended euclid (find reverse) tests passed.")

    # Find gcd
    assert gcd_extended_euclid(0, 0)[0] == 0
    assert gcd_extended_euclid(0, 1)[0] == 1
    assert gcd_extended_euclid(1, 0)[0] == 1
    assert gcd_extended_euclid(1, 1)[0] == 1
    assert gcd_extended_euclid(2, 3)[0] == 1
    assert gcd_extended_euclid(2, 5)[0] == 1
    assert gcd_extended_euclid(5, 11)[0] == 1
    assert gcd_extended_euclid(3, 20)[0] == 1
    assert gcd_extended_euclid(9, 13)[0] == 1
    assert gcd_extended_euclid(6, 9)[0] == 3
    assert gcd_extended_euclid(12, 15)[0] == 3
    assert gcd_extended_euclid(14, 21)[0] == 7
    assert gcd_extended_euclid(18, 24)[0] == 6
    assert gcd_extended_euclid(35, 49)[0] == 7
    assert gcd_extended_euclid(27, 36)[0] == 9
    assert gcd_extended_euclid(20, 30)[0] == 10
    assert gcd_extended_euclid(25, 35)[0] == 5
    assert gcd_extended_euclid(40, 60)[0] == 20
    assert gcd_extended_euclid(50, 75)[0] == 25
    print("All gcd extended euclid tests passed.")

    print("All tests passed.")

if __name__ == '__main__':
    main()
