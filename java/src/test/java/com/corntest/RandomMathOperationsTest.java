package com.corntest;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Test class for RandomMathOperations.
 * These tests are intentionally flaky to test flake detection systems.
 * 
 * - generateRandomOddNumber() test fails ~25% of the time
 * - generateRandomEvenNumber() test fails ~50% of the time
 * - generateRandomPrimeCandidate() test fails ~75% of the time
 */
@DisplayName("RandomMathOperations Tests (Intentionally Flaky)")
class RandomMathOperationsTest {

    private final RandomMathOperations randomOps = new RandomMathOperations();

    @RepeatedTest(value = 20, name = "Run {currentRepetition}/{totalRepetitions}")
    @DisplayName("Random odd number should be odd (Flaky: fails ~25% of the time)")
    void testGenerateRandomOddNumber() {
        int number = randomOps.generateRandomOddNumber();
        assertTrue(number >= 1 && number <= 100, "Number should be between 1 and 100");
        assertTrue(number % 2 == 1, "Number should be odd, but got: " + number);
    }

    @RepeatedTest(value = 20, name = "Run {currentRepetition}/{totalRepetitions}")
    @DisplayName("Random even number should be even (Flaky: fails ~50% of the time)")
    void testGenerateRandomEvenNumber() {
        int number = randomOps.generateRandomEvenNumber();
        assertTrue(number >= 0 && number <= 100, "Number should be between 0 and 100");
        assertTrue(number % 2 == 0, "Number should be even, but got: " + number);
    }

    @RepeatedTest(value = 20, name = "Run {currentRepetition}/{totalRepetitions}")
    @DisplayName("Random prime candidate should be prime (Flaky: fails ~75% of the time)")
    void testGenerateRandomPrimeCandidate() {
        int number = randomOps.generateRandomPrimeCandidate();
        assertTrue(number >= 2 && number <= 200, "Number should be between 2 and 200");
        assertTrue(RandomMathOperations.isPrime(number), "Number should be prime, but got: " + number);
    }

    @Test
    @DisplayName("Helper method isPrime should correctly identify prime numbers")
    void testIsPrime() {
        // Test prime numbers
        assertTrue(RandomMathOperations.isPrime(2));
        assertTrue(RandomMathOperations.isPrime(3));
        assertTrue(RandomMathOperations.isPrime(5));
        assertTrue(RandomMathOperations.isPrime(7));
        assertTrue(RandomMathOperations.isPrime(11));
        assertTrue(RandomMathOperations.isPrime(97));

        // Test non-prime numbers
        assertFalse(RandomMathOperations.isPrime(1));
        assertFalse(RandomMathOperations.isPrime(4));
        assertFalse(RandomMathOperations.isPrime(6));
        assertFalse(RandomMathOperations.isPrime(9));
        assertFalse(RandomMathOperations.isPrime(100));
    }
}
