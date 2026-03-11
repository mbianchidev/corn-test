#include <gtest/gtest.h>
#include "random_math_operations.h"

class RandomMathOperationsTest : public ::testing::Test {
protected:
    RandomMathOperations rng;
};

// Odd number tests — 20 iterations each (always passes, no flaw)
TEST_F(RandomMathOperationsTest, OddNumberIsOdd) {
    for (int i = 0; i < 20; ++i) {
        int value = rng.generateRandomOddNumber();
        EXPECT_EQ(value % 2, 1) << "Iteration " << i << ": " << value << " is not odd";
    }
}

TEST_F(RandomMathOperationsTest, OddNumberInRange) {
    for (int i = 0; i < 20; ++i) {
        int value = rng.generateRandomOddNumber();
        EXPECT_GE(value, 1) << "Iteration " << i;
        EXPECT_LE(value, 99) << "Iteration " << i;
    }
}

// Even number tests — 20 iterations each (flaky due to 5% flaw)
TEST_F(RandomMathOperationsTest, EvenNumberIsEven) {
    for (int i = 0; i < 20; ++i) {
        int value = rng.generateRandomEvenNumber();
        EXPECT_EQ(value % 2, 0) << "Iteration " << i << ": " << value << " is not even";
    }
}

TEST_F(RandomMathOperationsTest, EvenNumberInRange) {
    for (int i = 0; i < 20; ++i) {
        int value = rng.generateRandomEvenNumber();
        EXPECT_GE(value, 0) << "Iteration " << i;
        EXPECT_LE(value, 100) << "Iteration " << i;
    }
}

// Prime candidate tests — 20 iterations each (always passes, no flaw)
TEST_F(RandomMathOperationsTest, PrimeCandidateIsPrime) {
    for (int i = 0; i < 20; ++i) {
        int value = rng.generateRandomPrimeCandidate();
        EXPECT_TRUE(RandomMathOperations::isPrime(value))
            << "Iteration " << i << ": " << value << " is not prime";
    }
}

TEST_F(RandomMathOperationsTest, PrimeCandidateInRange) {
    for (int i = 0; i < 20; ++i) {
        int value = rng.generateRandomPrimeCandidate();
        EXPECT_GE(value, 2) << "Iteration " << i;
        EXPECT_LE(value, 97) << "Iteration " << i;
    }
}

// isPrime deterministic tests
TEST_F(RandomMathOperationsTest, IsPrimeKnownPrimes) {
    EXPECT_TRUE(RandomMathOperations::isPrime(2));
    EXPECT_TRUE(RandomMathOperations::isPrime(3));
    EXPECT_TRUE(RandomMathOperations::isPrime(5));
    EXPECT_TRUE(RandomMathOperations::isPrime(7));
    EXPECT_TRUE(RandomMathOperations::isPrime(11));
    EXPECT_TRUE(RandomMathOperations::isPrime(97));
}

TEST_F(RandomMathOperationsTest, IsPrimeKnownNonPrimes) {
    EXPECT_FALSE(RandomMathOperations::isPrime(0));
    EXPECT_FALSE(RandomMathOperations::isPrime(1));
    EXPECT_FALSE(RandomMathOperations::isPrime(4));
    EXPECT_FALSE(RandomMathOperations::isPrime(6));
    EXPECT_FALSE(RandomMathOperations::isPrime(9));
    EXPECT_FALSE(RandomMathOperations::isPrime(100));
    EXPECT_FALSE(RandomMathOperations::isPrime(-5));
}
