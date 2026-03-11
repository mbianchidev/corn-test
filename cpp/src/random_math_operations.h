#ifndef RANDOM_MATH_OPERATIONS_H
#define RANDOM_MATH_OPERATIONS_H

#include <random>

class RandomMathOperations {
public:
    RandomMathOperations();
    explicit RandomMathOperations(unsigned int seed);

    int generateRandomOddNumber();
    int generateRandomEvenNumber();
    int generateRandomPrimeCandidate();

    static bool isPrime(int n);

private:
    std::mt19937 gen;
};

#endif // RANDOM_MATH_OPERATIONS_H
