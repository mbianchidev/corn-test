"""Deterministic mathematical operations module.

This module provides a MathOperations class with pure, deterministic
mathematical functions that always return the same results for the same inputs.
"""

import math


class MathOperations:
    """A collection of deterministic mathematical operations."""

    def add(self, a: int, b: int) -> int:
        """Add two integers.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            The sum of a and b.
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract two integers.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            The difference of a and b.
        """
        return a - b

    def multiply(self, a: int, b: int) -> int:
        """Multiply two integers.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            The product of a and b.
        """
        return a * b

    def divide(self, a: int, b: int) -> float:
        """Divide two integers.

        Args:
            a: Numerator.
            b: Denominator.

        Returns:
            The quotient of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def power(self, base: float, exponent: int) -> float:
        """Calculate base raised to the power of exponent.

        Args:
            base: The base value.
            exponent: The exponent value.

        Returns:
            base raised to the power of exponent.
        """
        return math.pow(base, exponent)

    def factorial(self, n: int) -> int:
        """Calculate the factorial of a non-negative integer.

        Args:
            n: A non-negative integer.

        Returns:
            The factorial of n.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def derivative(self, coefficients: list[float]) -> list[float]:
        """Compute the derivative of a polynomial.

        The polynomial is represented by its coefficients where the index
        corresponds to the power of x. For example, [3, 2, 1] represents
        3 + 2x + x^2, and its derivative is [2, 2].

        Args:
            coefficients: List of polynomial coefficients, where index i
                corresponds to the coefficient of x^i.

        Returns:
            List of coefficients for the derivative polynomial.
        """
        if len(coefficients) <= 1:
            return [0.0]
        return [i * coefficients[i] for i in range(1, len(coefficients))]

    def pi(self) -> str:
        """Return pi as a string with 40 decimal places.

        Returns:
            A string representation of pi with 40 decimal places.
        """
        return "3.1415926535897932384626433832795028841971"

    def gcd(self, a: int, b: int) -> int:
        """Calculate the greatest common divisor using the Euclidean algorithm.

        Handles negative numbers by taking absolute values.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            The greatest common divisor of a and b.
        """
        a = abs(a)
        b = abs(b)
        while b != 0:
            a, b = b, a % b
        return a
