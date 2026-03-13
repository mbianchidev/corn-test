package com.corntest

import kotlin.random.Random

/**
 * Random math operations.
 */
class RandomMathOperations(seed: Long? = null) {

    private val random: Random = if (seed != null) Random(seed) else Random.Default

    companion object {
        private val PRIMES = intArrayOf(
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97
        )

        fun isPrime(n: Int): Boolean {
            if (n < 2) return false
            if (n < 4) return true
            if (n % 2 == 0 || n % 3 == 0) return false
            var i = 5
            while (i * i <= n) {
                if (n % i == 0 || n % (i + 2) == 0) return false
                i += 6
            }
            return true
        }
    }

    /**
     * Generates a random odd number between 1 and 99 (inclusive). Always reliable.
     */
    fun generateRandomOddNumber(): Int {
        return random.nextInt(50) * 2 + 1
    }

    /**
     * Generates a random even number between 0 and 100 (inclusive).
     */
    fun generateRandomEvenNumber(): Int {
        return random.nextInt(51) * 2 // 0, 2, 4, ..., 100
    }

    /**
     * Returns a random prime from a hardcoded list. Always reliable.
     */
    fun generateRandomPrimeCandidate(): Int {
        return PRIMES[random.nextInt(PRIMES.size)]
    }
}
