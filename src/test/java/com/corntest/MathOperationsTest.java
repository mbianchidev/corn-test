package com.corntest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Test class for MathOperations.
 * These tests are deterministic and should always pass.
 */
@DisplayName("MathOperations Tests")
class MathOperationsTest {

    private MathOperations mathOps;

    @BeforeEach
    void setUp() {
        mathOps = new MathOperations();
    }

    @Test
    @DisplayName("Addition should correctly add two positive numbers")
    void testAddPositiveNumbers() {
        assertEquals(5, mathOps.add(2, 3));
        assertEquals(100, mathOps.add(40, 60));
    }

    @Test
    @DisplayName("Addition should correctly handle negative numbers")
    void testAddNegativeNumbers() {
        assertEquals(-5, mathOps.add(-2, -3));
        assertEquals(0, mathOps.add(5, -5));
    }

    @Test
    @DisplayName("Subtraction should correctly subtract two numbers")
    void testSubtract() {
        assertEquals(2, mathOps.subtract(5, 3));
        assertEquals(-2, mathOps.subtract(3, 5));
        assertEquals(0, mathOps.subtract(10, 10));
    }

    @Test
    @DisplayName("Multiplication should correctly multiply two numbers")
    void testMultiply() {
        assertEquals(6, mathOps.multiply(2, 3));
        assertEquals(-6, mathOps.multiply(-2, 3));
        assertEquals(0, mathOps.multiply(0, 100));
    }

    @Test
    @DisplayName("Division should correctly divide two numbers")
    void testDivide() {
        assertEquals(2.0, mathOps.divide(6, 3), 0.001);
        assertEquals(2.5, mathOps.divide(5, 2), 0.001);
        assertEquals(-2.0, mathOps.divide(6, -3), 0.001);
    }

    @Test
    @DisplayName("Division by zero should throw ArithmeticException")
    void testDivideByZero() {
        assertThrows(ArithmeticException.class, () -> mathOps.divide(5, 0));
    }

    @Test
    @DisplayName("Power should correctly calculate exponentials")
    void testPower() {
        assertEquals(8.0, mathOps.power(2, 3), 0.001);
        assertEquals(1.0, mathOps.power(5, 0), 0.001);
        assertEquals(0.25, mathOps.power(2, -2), 0.001);
    }

    @Test
    @DisplayName("Factorial should correctly calculate factorials")
    void testFactorial() {
        assertEquals(1, mathOps.factorial(0));
        assertEquals(1, mathOps.factorial(1));
        assertEquals(2, mathOps.factorial(2));
        assertEquals(6, mathOps.factorial(3));
        assertEquals(24, mathOps.factorial(4));
        assertEquals(120, mathOps.factorial(5));
    }

    @Test
    @DisplayName("Factorial with negative number should throw IllegalArgumentException")
    void testFactorialNegative() {
        assertThrows(IllegalArgumentException.class, () -> mathOps.factorial(-1));
    }

    @Test
    @DisplayName("GCD should correctly calculate greatest common divisor")
    void testGcd() {
        assertEquals(1, mathOps.gcd(1, 1));
        assertEquals(5, mathOps.gcd(10, 15));
        assertEquals(6, mathOps.gcd(48, 18));
        assertEquals(1, mathOps.gcd(17, 19));
    }

    @Test
    @DisplayName("GCD should handle negative numbers")
    void testGcdNegative() {
        assertEquals(5, mathOps.gcd(-10, 15));
        assertEquals(6, mathOps.gcd(48, -18));
        assertEquals(7, mathOps.gcd(-14, -21));
    }

    @Test
    @DisplayName("Derivative of a polynomial should return correct coefficients")
    void testDerivative() {
        // derivative of 3 + 2x + 5x^2 = 2 + 10x
        assertArrayEquals(new double[]{2, 10}, mathOps.derivative(new double[]{3, 2, 5}), 0.001);
        // derivative of x^3 = 3x^2
        assertArrayEquals(new double[]{0, 0, 3}, mathOps.derivative(new double[]{0, 0, 0, 1}), 0.001);
        // derivative of 7 = 0
        assertArrayEquals(new double[]{0}, mathOps.derivative(new double[]{7}), 0.001);
    }

    @Test
    @DisplayName("Derivative of empty polynomial should return zero")
    void testDerivativeEmpty() {
        assertArrayEquals(new double[]{0}, mathOps.derivative(new double[]{}), 0.001);
    }

    @Test
    @DisplayName("Derivative with null coefficients should throw IllegalArgumentException")
    void testDerivativeNull() {
        assertThrows(IllegalArgumentException.class, () -> mathOps.derivative(null));
    }
}
