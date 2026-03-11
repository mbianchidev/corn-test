<?php

declare(strict_types=1);

namespace CornTest\Tests;

use CornTest\RandomMathOperations;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

class RandomMathOperationsTest extends TestCase
{
    private RandomMathOperations $randomOps;

    protected function setUp(): void
    {
        $this->randomOps = new RandomMathOperations();
    }

    /** @return array<string, array{int}> */
    public static function iterationProvider(): array
    {
        $data = [];
        for ($i = 1; $i <= 20; $i++) {
            $data["iteration $i"] = [$i];
        }
        return $data;
    }

    // --- Random Odd Number (Reliable) ---

    #[Test]
    #[DataProvider('iterationProvider')]
    public function randomOddNumberShouldBeOdd(int $iteration): void
    {
        $number = $this->randomOps->generateRandomOddNumber();
        $this->assertTrue(
            $number % 2 === 1,
            "Number should be odd, but got: $number"
        );
    }

    #[Test]
    #[DataProvider('iterationProvider')]
    public function randomOddNumberShouldBeInRange(int $iteration): void
    {
        $number = $this->randomOps->generateRandomOddNumber();
        $this->assertGreaterThanOrEqual(1, $number, "Number should be >= 1, but got: $number");
        $this->assertLessThanOrEqual(99, $number, "Number should be <= 99, but got: $number");
    }

    // --- Random Even Number (Flaky - 5% chance of failure per iteration) ---

    #[Test]
    #[DataProvider('iterationProvider')]
    public function randomEvenNumberShouldBeEven(int $iteration): void
    {
        $number = $this->randomOps->generateRandomEvenNumber();
        $this->assertTrue(
            $number % 2 === 0,
            "Number should be even, but got: $number"
        );
    }

    #[Test]
    #[DataProvider('iterationProvider')]
    public function randomEvenNumberShouldBeInRange(int $iteration): void
    {
        $number = $this->randomOps->generateRandomEvenNumber();
        $this->assertGreaterThanOrEqual(0, $number, "Number should be >= 0, but got: $number");
        $this->assertLessThanOrEqual(100, $number, "Number should be <= 100, but got: $number");
    }

    // --- Random Prime Candidate (Reliable) ---

    #[Test]
    #[DataProvider('iterationProvider')]
    public function randomPrimeCandidateShouldBePrime(int $iteration): void
    {
        $number = $this->randomOps->generateRandomPrimeCandidate();
        $this->assertTrue(
            RandomMathOperations::isPrime($number),
            "Number should be prime, but got: $number"
        );
    }

    #[Test]
    #[DataProvider('iterationProvider')]
    public function randomPrimeCandidateShouldBeInRange(int $iteration): void
    {
        $number = $this->randomOps->generateRandomPrimeCandidate();
        $this->assertGreaterThanOrEqual(2, $number, "Number should be >= 2, but got: $number");
        $this->assertLessThanOrEqual(97, $number, "Number should be <= 97, but got: $number");
    }

    // --- isPrime helper ---

    #[Test]
    public function isPrimeReturnsTrueForPrimes(): void
    {
        $primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97];
        foreach ($primes as $prime) {
            $this->assertTrue(
                RandomMathOperations::isPrime($prime),
                "$prime should be prime"
            );
        }
    }

    #[Test]
    public function isPrimeReturnsFalseForNonPrimes(): void
    {
        $nonPrimes = [0, 1, 4, 6, 8, 9, 10, 15, 100];
        foreach ($nonPrimes as $nonPrime) {
            $this->assertFalse(
                RandomMathOperations::isPrime($nonPrime),
                "$nonPrime should not be prime"
            );
        }
    }
}
