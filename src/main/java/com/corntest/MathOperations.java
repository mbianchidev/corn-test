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
     * Computes the derivative of a polynomial represented by its coefficients.
     * The coefficients array represents the polynomial:
     *   coefficients[0] + coefficients[1]*x + coefficients[2]*x^2 + ... + coefficients[n]*x^n
     *
     * @param coefficients the polynomial coefficients in ascending order of degree
     * @return the coefficients of the derivative polynomial
     * @throws IllegalArgumentException if coefficients is null
     */
    public double[] derivative(double[] coefficients) {
        if (coefficients == null) {
            throw new IllegalArgumentException("Coefficients array must not be null");
        }
        if (coefficients.length <= 1) {
            return new double[]{0};
        }
        double[] result = new double[coefficients.length - 1];
        for (int i = 1; i < coefficients.length; i++) {
            result[i - 1] = coefficients[i] * i;
        }
        return result;
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
