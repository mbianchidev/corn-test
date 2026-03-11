<?php

declare(strict_types=1);

namespace CornTest;

use InvalidArgumentException;

class MathOperations
{
    public function add(int $a, int $b): int
    {
        return $a + $b;
    }

    public function subtract(int $a, int $b): int
    {
        return $a - $b;
    }

    public function multiply(int $a, int $b): int
    {
        return $a * $b;
    }

    public function divide(int $a, int $b): float
    {
        if ($b === 0) {
            throw new InvalidArgumentException('Division by zero is not allowed');
        }

        return $a / $b;
    }

    public function power(float $base, int $exponent): float
    {
        return pow($base, $exponent);
    }

    public function factorial(int $n): int
    {
        if ($n < 0) {
            throw new InvalidArgumentException('Factorial is not defined for negative numbers');
        }

        if ($n === 0 || $n === 1) {
            return 1;
        }

        $result = 1;
        for ($i = 2; $i <= $n; $i++) {
            $result *= $i;
        }

        return $result;
    }

    /**
     * Compute the derivative of a polynomial.
     * Coefficients are in ascending power order: index i = coefficient of x^i.
     *
     * @param float[] $coefficients
     * @return float[]
     */
    public function derivative(array $coefficients): array
    {
        if ($coefficients === []) {
            throw new InvalidArgumentException('Coefficients array must not be empty');
        }

        if (count($coefficients) <= 1) {
            return [0.0];
        }

        $result = [];
        for ($i = 1; $i < count($coefficients); $i++) {
            $result[] = $coefficients[$i] * $i;
        }

        return $result;
    }

    public function pi(): string
    {
        return '3.1415926535897932384626433832795028841971';
    }

    public function gcd(int $a, int $b): int
    {
        $a = abs($a);
        $b = abs($b);

        while ($b !== 0) {
            $temp = $b;
            $b = $a % $b;
            $a = $temp;
        }

        return $a;
    }
}
