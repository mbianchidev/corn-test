package com.corntest

/**
 * Deterministic math operations for reliable testing.
 */
class MathOperations {

    fun add(a: Int, b: Int): Int = a + b

    fun subtract(a: Int, b: Int): Int = a - b

    fun multiply(a: Int, b: Int): Int = a * b

    fun divide(a: Int, b: Int): Double {
        if (b == 0) throw ArithmeticException("Division by zero")
        return a.toDouble() / b.toDouble()
    }

    fun power(base: Double, exponent: Int): Double {
        var result = 1.0
        val exp = if (exponent < 0) -exponent else exponent
        for (i in 0 until exp) {
            result *= base
        }
        return if (exponent < 0) 1.0 / result else result
    }

    fun factorial(n: Int): Long {
        if (n < 0) throw IllegalArgumentException("Factorial is not defined for negative numbers")
        var result = 1L
        for (i in 2..n) {
            result *= i
        }
        return result
    }

    fun derivative(coefficients: DoubleArray): DoubleArray {
        if (coefficients.size <= 1) return doubleArrayOf(0.0)
        return DoubleArray(coefficients.size - 1) { i ->
            coefficients[i + 1] * (i + 1)
        }
    }

    fun pi(): String = "3.1415926535897932384626433832795028841971"

    fun gcd(a: Int, b: Int): Int {
        var x = if (a < 0) -a else a
        var y = if (b < 0) -b else b
        while (y != 0) {
            val temp = y
            y = x % y
            x = temp
        }
        return x
    }
}
