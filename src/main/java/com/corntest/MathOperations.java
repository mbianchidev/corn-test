package com.corntest;

/**
 * Class containing deterministic mathematical operations.
 */
public class MathOperations {

    /**
     * Adds two integers.
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * Subtracts two integers.
     */
    public int subtract(int a, int b) {
        return a - b;
    }

    /**
     * Multiplies two integers.
     */
    public int multiply(int a, int b) {
        return a * b;
    }

    /**
     * Divides two integers.
     * @throws ArithmeticException if divisor is zero
     */
    public double divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return (double) a / b;
    }

    /**
     * Calculates the power of a number.
     */
    public double power(double base, int exponent) {
        return Math.pow(base, exponent);
    }

    /**
     * Calculates the factorial of a number.
     * @throws IllegalArgumentException if n is negative
     */
    public long factorial(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Factorial is not defined for negative numbers");
        }
        if (n == 0 || n == 1) {
            return 1;
        }
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    /**
     * Computes the nth value in the Fibonacci sequence.
     * The sequence starts with fibonacci(0)=0 and fibonacci(1)=1.
     * @throws IllegalArgumentException if n is negative
     */
    public long fibonacci(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Fibonacci is not defined for negative indices");
        }
        if (n <= 1) {
            return n;
        }
        long previous = 0;
        long current = 1;
        for (int step = 2; step <= n; step++) {
            long next = previous + current;
            previous = current;
            current = next;
        }
        return current;
    }

    /**
     * Calculates the greatest common divisor of two numbers using Euclidean algorithm.
     */
    public int gcd(int a, int b) {
        a = Math.abs(a);
        b = Math.abs(b);
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
}
