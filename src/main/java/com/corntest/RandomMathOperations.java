package com.corntest;

import java.util.Random;

/**
 * Class containing probabilistic mathematical operations.
 * These methods are designed to produce flaky test results for testing purposes.
 */
public class RandomMathOperations {

    private final Random random;

    public RandomMathOperations() {
        this.random = new Random();
    }

    public RandomMathOperations(long seed) {
        this.random = new Random(seed);
    }

    /**
     * Generates a random odd number between 1 and 100.
     * This implementation has a built-in flaw to make tests fail 25% of the time.
     * 
     * @return a number that SHOULD be odd, but occasionally returns an even number
     */
    public int generateRandomOddNumber() {
        int number = random.nextInt(50) * 2 + 1; // Generates odd number: 1, 3, 5, ..., 99
        
        // Intentional flaw: 25% of the time, add 1 to make it even
        if (random.nextDouble() < 0.25) {
            number += 1;
        }
        
        return number;
    }

    /**
     * Generates a random even number between 0 and 100.
     * This implementation has a built-in flaw to make tests fail 50% of the time.
     * 
     * @return a number that SHOULD be even, but occasionally returns an odd number
     */
    public int generateRandomEvenNumber() {
        int number = random.nextInt(51) * 2; // Generates even number: 0, 2, 4, ..., 100
        
        // Intentional flaw: 50% of the time, add 1 to make it odd
        if (random.nextDouble() < 0.50) {
            number += 1;
        }
        
        return number;
    }

    /**
     * Generates a random prime candidate between 2 and 100.
     * This implementation has a built-in flaw to make tests fail 75% of the time.
     * 
     * @return a number that SHOULD be prime, but is often composite
     */
    public int generateRandomPrimeCandidate() {
        int[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97};
        int primeIndex = random.nextInt(primes.length);
        int number = primes[primeIndex];
        
        // Intentional flaw: 75% of the time, multiply by 2 to make it composite
        if (random.nextDouble() < 0.75) {
            number *= 2;
        }
        
        return number;
    }

    /**
     * Helper method to check if a number is prime.
     */
    public static boolean isPrime(int n) {
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
}
