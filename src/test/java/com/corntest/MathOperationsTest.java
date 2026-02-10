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
    @DisplayName("Fibonacci should return correct values for base cases")
    void testFibonacciBaseCases() {
        assertEquals(0, mathOps.fibonacci(0));
        assertEquals(1, mathOps.fibonacci(1));
    }

    @Test
    @DisplayName("Fibonacci should return correct values for larger indices")
    void testFibonacciLargerValues() {
        assertEquals(1, mathOps.fibonacci(2));
        assertEquals(2, mathOps.fibonacci(3));
        assertEquals(5, mathOps.fibonacci(5));
        assertEquals(13, mathOps.fibonacci(7));
        assertEquals(55, mathOps.fibonacci(10));
        assertEquals(6765, mathOps.fibonacci(20));
    }

    @Test
    @DisplayName("Fibonacci with negative index should throw IllegalArgumentException")
    void testFibonacciNegative() {
        assertThrows(IllegalArgumentException.class, () -> mathOps.fibonacci(-1));
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
}
