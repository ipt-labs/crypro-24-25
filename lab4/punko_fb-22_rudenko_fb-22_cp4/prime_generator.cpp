#include "prime_generator.h"

bool PrimeGenerator::rabinMillerTest(const mpz_class& n, int iterations = 5) {
    if (n <= 1) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    mpz_class d = n - 1;
    unsigned int s = 0;
    while (d % 2 == 0) {
        s++;
        d /= 2;
    }

    for (int i = 0; i < iterations; i++) {
        mpz_class a = rng.get_z_range(n - 4) + 2;
        mpz_class x;

        mpz_powm(x.get_mpz_t(), a.get_mpz_t(), d.get_mpz_t(), n.get_mpz_t());

        if (x == 1 || x == n - 1)
            continue;

        bool isProbablyComposite = true;

        for (unsigned int r = 1; r < s; r++) {
            mpz_powm_ui(x.get_mpz_t(), x.get_mpz_t(), 2, n.get_mpz_t());

            if (x == n - 1) {
                isProbablyComposite = false;
                break;
            }

            if (x == 1)
                return false;
        }

        if (isProbablyComposite)
            return false;
    }

    return true;
}

mpz_class PrimeGenerator::generatePrime(unsigned int bitLength) {
    while (true) {
        mpz_class candidate = rng.get_z_bits(bitLength);
            
        mpz_setbit(candidate.get_mpz_t(), bitLength - 1);
        mpz_setbit(candidate.get_mpz_t(), 0);
            
        if (rabinMillerTest(candidate)) {
            return candidate;
        }
    }
}
