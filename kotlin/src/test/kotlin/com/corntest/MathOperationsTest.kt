package com.corntest

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

class MathOperationsTest {

    private val math = MathOperations()

    @Test
    fun testAddPositiveNumbers() {
        assertEquals(5, math.add(2, 3))
    }

    @Test
    fun testAddNegativeNumbers() {
        assertEquals(-5, math.add(-2, -3))
    }

    @Test
    fun testAddMixed() {
        assertEquals(1, math.add(-2, 3))
    }

    @Test
    fun testSubtract() {
        assertEquals(1, math.subtract(3, 2))
    }

    @Test
    fun testSubtractNegativeResult() {
        assertEquals(-1, math.subtract(2, 3))
    }

    @Test
    fun testMultiply() {
        assertEquals(6, math.multiply(2, 3))
    }

    @Test
    fun testMultiplyByZero() {
        assertEquals(0, math.multiply(5, 0))
    }

    @Test
    fun testDivide() {
        assertEquals(2.5, math.divide(5, 2))
    }

    @Test
    fun testDivideByZero() {
        assertFailsWith<ArithmeticException> {
            math.divide(1, 0)
        }
    }

    @Test
    fun testPower() {
        assertEquals(8.0, math.power(2.0, 3))
    }

    @Test
    fun testPowerOfZero() {
        assertEquals(1.0, math.power(5.0, 0))
    }

    @Test
    fun testFactorial() {
        assertEquals(120L, math.factorial(5))
    }

    @Test
    fun testFactorialZero() {
        assertEquals(1L, math.factorial(0))
    }

    @Test
    fun testFactorialNegative() {
        assertFailsWith<IllegalArgumentException> {
            math.factorial(-1)
        }
    }

    @Test
    fun testDerivative() {
        // 3 + 2x + 5x^2 => 2 + 10x
        val result = math.derivative(doubleArrayOf(3.0, 2.0, 5.0))
        assertEquals(2, result.size)
        assertEquals(2.0, result[0])
        assertEquals(10.0, result[1])
    }

    @Test
    fun testDerivativeConstant() {
        val result = math.derivative(doubleArrayOf(7.0))
        assertEquals(1, result.size)
        assertEquals(0.0, result[0])
    }

    @Test
    fun testPi() {
        assertTrue(math.pi().startsWith("3.14159"))
    }

    @Test
    fun testGcd() {
        assertEquals(6, math.gcd(12, 18))
    }

    @Test
    fun testGcdCoprime() {
        assertEquals(1, math.gcd(7, 13))
    }
}
