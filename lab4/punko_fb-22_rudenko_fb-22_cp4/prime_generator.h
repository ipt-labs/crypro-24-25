#include "headers.h"

class PrimeGenerator {
private:
    gmp_randclass rng;
    bool rabinMillerTest(const mpz_class& n, int iterations);
public:
    PrimeGenerator() : rng(gmp_randinit_default) {
        auto seed = std::chrono::high_resolution_clock::now().time_since_epoch().count();
        rng.seed(seed);
    }

    mpz_class generatePrime(unsigned int bitLength);
};
