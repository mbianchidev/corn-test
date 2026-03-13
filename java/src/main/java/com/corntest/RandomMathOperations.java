package com.corntest;

import java.util.Random;

/**
 * Class containing random mathematical operations.
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
     * 
     * @return a random odd number between 1 and 99
     */
    public int generateRandomOddNumber() {
        int number = random.nextInt(50) * 2 + 1; // Generates odd number: 1, 3, 5, ..., 99
        return number;
    }

    /**
     * Generates a random even number between 0 and 100.
     * 
     * @return a random even number between 0 and 100
     */
    public int generateRandomEvenNumber() {
        int number = random.nextInt(51) * 2; // Generates even number: 0, 2, 4, ..., 100
        return number;
    }

    /**
     * Generates a random prime candidate between 2 and 97.
     * 
     * @return a random prime number between 2 and 97
     */
    public int generateRandomPrimeCandidate() {
        int[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97};
        int primeIndex = random.nextInt(primes.length);
        return primes[primeIndex];
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
