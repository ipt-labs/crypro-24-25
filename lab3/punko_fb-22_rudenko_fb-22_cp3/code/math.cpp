#include "headers.h"

int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int inverseElement(int a, int alphLen) {
    if (alphLen <= 0) return -1;
    a = ((a % alphLen) + alphLen) % alphLen;
    if (gcd(a, alphLen) != 1) return -1;

    int prevCoef = 0, currCoef = 1;
    int prevRemainder = alphLen, currRemainder = a;

    while (currRemainder != 0) {
        int quotient = prevRemainder / currRemainder;

        int tempCoef = currCoef;
        currCoef = prevCoef - quotient * currCoef;
        prevCoef = tempCoef;

        int tempRemainder = currRemainder;
        currRemainder = prevRemainder - quotient * currRemainder;
        prevRemainder = tempRemainder;
    }

    if (prevCoef < 0) prevCoef += alphLen;
    return prevCoef;
}

std::vector<int> solveLinearCongruence(int a, int b, int n) {
    int GCD = gcd(a, n);

    if (GCD == 1) {
        int inv = inverseElement(a, n);
        return { (inv * b) % n };
    }

    if (b % GCD != 0) {
        return {};
    }
    a /= GCD;
    b /= GCD;
    n /= GCD;

    int x0 = (inverseElement(a, n) * b) % n;

    std::vector<int> solutions;
    for (int i = 0; i < GCD; ++i) {
        solutions.push_back((x0 + i * n) % (n * GCD));
    }

    return solutions;
}