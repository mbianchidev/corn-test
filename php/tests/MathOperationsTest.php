<?php

declare(strict_types=1);

namespace CornTest\Tests;

use CornTest\MathOperations;
use InvalidArgumentException;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

class MathOperationsTest extends TestCase
{
    private MathOperations $mathOps;

    protected function setUp(): void
    {
        $this->mathOps = new MathOperations();
    }

    // --- Addition ---

    /** @return array<string, array{int, int, int}> */
    public static function additionProvider(): array
    {
        return [
            'positive numbers'     => [2, 3, 5],
            'large numbers'        => [40, 60, 100],
            'negative numbers'     => [-5, -3, -8],
            'mixed sign'           => [-10, 5, -5],
            'zero and positive'    => [0, 7, 7],
            'zero and zero'        => [0, 0, 0],
        ];
    }

    #[Test]
    #[DataProvider('additionProvider')]
    public function additionReturnsCorrectResult(int $a, int $b, int $expected): void
    {
        $this->assertSame($expected, $this->mathOps->add($a, $b));
    }

    // --- Subtraction ---

    /** @return array<string, array{int, int, int}> */
    public static function subtractionProvider(): array
    {
        return [
            'positive result'   => [10, 3, 7],
            'negative result'   => [3, 10, -7],
            'zeros'             => [0, 0, 0],
            'negative numbers'  => [-5, -3, -2],
        ];
    }

    #[Test]
    #[DataProvider('subtractionProvider')]
    public function subtractionReturnsCorrectResult(int $a, int $b, int $expected): void
    {
        $this->assertSame($expected, $this->mathOps->subtract($a, $b));
    }

    // --- Multiplication ---

    /** @return array<string, array{int, int, int}> */
    public static function multiplicationProvider(): array
    {
        return [
            'positive numbers'  => [4, 5, 20],
            'with zero'         => [0, 100, 0],
            'negative numbers'  => [-3, -4, 12],
            'mixed sign'        => [-3, 4, -12],
        ];
    }

    #[Test]
    #[DataProvider('multiplicationProvider')]
    public function multiplicationReturnsCorrectResult(int $a, int $b, int $expected): void
    {
        $this->assertSame($expected, $this->mathOps->multiply($a, $b));
    }

    // --- Division ---

    /** @return array<string, array{int, int, float}> */
    public static function divisionProvider(): array
    {
        return [
            'exact division'   => [10, 2, 5.0],
            'decimal result'   => [7, 2, 3.5],
            'negative result'  => [-10, 2, -5.0],
        ];
    }

    #[Test]
    #[DataProvider('divisionProvider')]
    public function divisionReturnsCorrectResult(int $a, int $b, float $expected): void
    {
        $this->assertEqualsWithDelta($expected, $this->mathOps->divide($a, $b), 0.0001);
    }

    #[Test]
    public function divisionByZeroThrowsException(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->mathOps->divide(10, 0);
    }

    // --- Power ---

    /** @return array<string, array{float, int, float}> */
    public static function powerProvider(): array
    {
        return [
            'square'           => [2.0, 3, 8.0],
            'zero exponent'    => [5.0, 0, 1.0],
            'base one'         => [1.0, 100, 1.0],
            'negative exp'     => [2.0, -1, 0.5],
        ];
    }

    #[Test]
    #[DataProvider('powerProvider')]
    public function powerReturnsCorrectResult(float $base, int $exponent, float $expected): void
    {
        $this->assertEqualsWithDelta($expected, $this->mathOps->power($base, $exponent), 0.0001);
    }

    // --- Factorial ---

    /** @return array<string, array{int, int}> */
    public static function factorialProvider(): array
    {
        return [
            'zero'   => [0, 1],
            'one'    => [1, 1],
            'five'   => [5, 120],
            'ten'    => [10, 3628800],
        ];
    }

    #[Test]
    #[DataProvider('factorialProvider')]
    public function factorialReturnsCorrectResult(int $n, int $expected): void
    {
        $this->assertSame($expected, $this->mathOps->factorial($n));
    }

    #[Test]
    public function factorialOfNegativeThrowsException(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->mathOps->factorial(-1);
    }

    // --- Derivative ---

    /** @return array<string, array{float[], float[]}> */
    public static function derivativeProvider(): array
    {
        return [
            'constant'     => [[5.0], [0.0]],
            'linear'       => [[3.0, 2.0], [2.0]],
            'quadratic'    => [[1.0, 0.0, 3.0], [0.0, 6.0]],
            'cubic'        => [[2.0, 3.0, 0.0, 1.0], [3.0, 0.0, 3.0]],
        ];
    }

    #[Test]
    #[DataProvider('derivativeProvider')]
    public function derivativeReturnsCorrectResult(array $coefficients, array $expected): void
    {
        $result = $this->mathOps->derivative($coefficients);
        $this->assertCount(count($expected), $result);
        for ($i = 0; $i < count($expected); $i++) {
            $this->assertEqualsWithDelta($expected[$i], $result[$i], 0.0001);
        }
    }

    #[Test]
    public function derivativeOfEmptyThrowsException(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->mathOps->derivative([]);
    }

    // --- Pi ---

    #[Test]
    public function piReturnsCorrectValue(): void
    {
        $this->assertStringStartsWith('3.14159265', $this->mathOps->pi());
    }

    // --- GCD ---

    /** @return array<string, array{int, int, int}> */
    public static function gcdProvider(): array
    {
        return [
            'coprime'          => [7, 13, 1],
            'common factor'    => [12, 8, 4],
            'same numbers'     => [5, 5, 5],
            'one and number'   => [1, 99, 1],
            'with zero'        => [0, 5, 5],
            'negative numbers' => [-12, 8, 4],
        ];
    }

    #[Test]
    #[DataProvider('gcdProvider')]
    public function gcdReturnsCorrectResult(int $a, int $b, int $expected): void
    {
        $this->assertSame($expected, $this->mathOps->gcd($a, $b));
    }
}
