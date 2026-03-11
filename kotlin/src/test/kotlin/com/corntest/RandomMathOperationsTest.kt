package com.corntest

import kotlin.test.Test
import kotlin.test.assertTrue
import kotlin.test.assertEquals

class RandomMathOperationsTest {

    @Test
    fun testGenerateRandomOddNumber() {
        val rng = RandomMathOperations()
        repeat(20) { iteration ->
            val result = rng.generateRandomOddNumber()
            assertTrue(
                result % 2 != 0,
                "Iteration $iteration: Expected odd number but got $result"
            )
            assertTrue(
                result in 1..99,
                "Iteration $iteration: Expected value in 1..99 but got $result"
            )
        }
    }

    @Test
    fun testGenerateRandomEvenNumber() {
        val rng = RandomMathOperations()
        repeat(20) { iteration ->
            val result = rng.generateRandomEvenNumber()
            assertEquals(
                0, result % 2,
                "Iteration $iteration: Expected even number but got $result"
            )
            assertTrue(
                result in 0..100,
                "Iteration $iteration: Expected value in 0..100 but got $result"
            )
        }
    }

    @Test
    fun testGenerateRandomPrimeCandidate() {
        val rng = RandomMathOperations()
        repeat(20) { iteration ->
            val result = rng.generateRandomPrimeCandidate()
            assertTrue(
                RandomMathOperations.isPrime(result),
                "Iteration $iteration: Expected prime but got $result"
            )
            assertTrue(
                result in 2..97,
                "Iteration $iteration: Expected value in 2..97 but got $result"
            )
        }
    }

    @Test
    fun testIsPrimeWithKnownPrimes() {
        val primes = listOf(2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
        for (p in primes) {
            assertTrue(RandomMathOperations.isPrime(p), "$p should be prime")
        }
    }

    @Test
    fun testIsPrimeWithNonPrimes() {
        val nonPrimes = listOf(0, 1, 4, 6, 8, 9, 10, 12, 15, 100)
        for (n in nonPrimes) {
            assertTrue(!RandomMathOperations.isPrime(n), "$n should not be prime")
        }
    }
}
