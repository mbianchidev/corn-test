<?php

declare(strict_types=1);

namespace CornTest;

class RandomMathOperations
{
    private const array PRIMES = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97,
    ];

    /**
     * Generate a random odd number between 1 and 99.
     */
    public function generateRandomOddNumber(): int
    {
        return mt_rand(0, 49) * 2 + 1;
    }

    /**
     * Generate a random even number between 0 and 100.
     */
    public function generateRandomEvenNumber(): int
    {
        return mt_rand(0, 50) * 2;
    }

    /**
     * Generate a random prime candidate from the list of known primes.
     */
    public function generateRandomPrimeCandidate(): int
    {
        $index = mt_rand(0, count(self::PRIMES) - 1);
        return self::PRIMES[$index];
    }

    /**
     * Check if a number is prime using trial division.
     */
    public static function isPrime(int $n): bool
    {
        if ($n < 2) {
            return false;
        }

        if ($n < 4) {
            return true;
        }

        if ($n % 2 === 0 || $n % 3 === 0) {
            return false;
        }

        for ($i = 5; $i * $i <= $n; $i += 6) {
            if ($n % $i === 0 || $n % ($i + 2) === 0) {
                return false;
            }
        }

        return true;
    }
}
