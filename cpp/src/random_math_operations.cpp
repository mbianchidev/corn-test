#include "random_math_operations.h"

RandomMathOperations::RandomMathOperations()
    : gen(std::random_device{}()) {}

RandomMathOperations::RandomMathOperations(unsigned int seed)
    : gen(seed) {}

int RandomMathOperations::generateRandomOddNumber() {
    std::uniform_int_distribution<int> dist(0, 49);
    return dist(gen) * 2 + 1; // 1, 3, 5, ..., 99
}

int RandomMathOperations::generateRandomEvenNumber() {
    std::uniform_int_distribution<int> dist(0, 50);
    int number = dist(gen) * 2; // 0, 2, 4, ..., 100

    // Intentional flaw: 5% of the time, add 1 to make it odd
    std::uniform_real_distribution<> flaw(0.0, 1.0);
    if (flaw(gen) < 0.05) {
        number += 1;
    }

    return number;
}

int RandomMathOperations::generateRandomPrimeCandidate() {
    static const int primes[] = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97
    };
    std::uniform_int_distribution<int> dist(0, 24);
    return primes[dist(gen)];
}

bool RandomMathOperations::isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}
