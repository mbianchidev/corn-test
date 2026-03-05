"""
Module containing deterministic mathematical operations.
"""
import math


class MathOperations:
    """Class containing deterministic mathematical operations."""

    def add(self, a: int, b: int) -> int:
        """Adds two integers."""
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtracts two integers."""
        return a - b

    def multiply(self, a: int, b: int) -> int:
        """Multiplies two integers."""
        return a * b

    def divide(self, a: int, b: int) -> float:
        """Divides two numbers. Raises ZeroDivisionError if divisor is zero."""
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b

    def power(self, base: float, exponent: int) -> float:
        """Calculates the power of a number."""
        return math.pow(base, exponent)

    def factorial(self, n: int) -> int:
        """Calculates the factorial of a number. Raises ValueError if n is negative."""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def derivative(self, coefficients: list[float]) -> list[float]:
        """
        Computes the derivative of a polynomial represented by its coefficients.
        coefficients[0] + coefficients[1]*x + coefficients[2]*x^2 + ...
        """
        if coefficients is None:
            raise ValueError("Coefficients array must not be null")
        if len(coefficients) <= 1:
            return [0.0]
        result = []
        for i in range(1, len(coefficients)):
            result.append(coefficients[i] * i)
        return result

    def pi(self) -> str:
        """Returns the first 40 decimals of the pi constant."""
        return "3.1415926535897932384626433832795028841971"

    def gcd(self, a: int, b: int) -> int:
        """Calculates the greatest common divisor using Euclidean algorithm."""
        a = abs(a)
        b = abs(b)
        while b != 0:
            a, b = b, a % b
        return a
