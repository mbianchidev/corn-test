"""Pytest tests for MathOperations.

All tests are deterministic and should always pass.
"""

import pytest

from math_operations import MathOperations


@pytest.fixture
def math_ops():
    """Provide a MathOperations instance for each test."""
    return MathOperations()


# --- Addition ---

class TestAdd:
    """Tests for the add method."""

    @pytest.mark.parametrize("a, b, expected", [
        (1, 1, 2),
        (0, 0, 0),
        (-1, -1, -2),
        (-1, 1, 0),
        (100, 200, 300),
    ])
    def test_add(self, math_ops, a, b, expected):
        assert math_ops.add(a, b) == expected


# --- Subtraction ---

class TestSubtract:
    """Tests for the subtract method."""

    @pytest.mark.parametrize("a, b, expected", [
        (5, 3, 2),
        (0, 0, 0),
        (-1, -1, 0),
        (-1, 1, -2),
        (100, 200, -100),
    ])
    def test_subtract(self, math_ops, a, b, expected):
        assert math_ops.subtract(a, b) == expected


# --- Multiplication ---

class TestMultiply:
    """Tests for the multiply method."""

    @pytest.mark.parametrize("a, b, expected", [
        (2, 3, 6),
        (0, 5, 0),
        (-2, 3, -6),
        (-2, -3, 6),
        (100, 100, 10000),
    ])
    def test_multiply(self, math_ops, a, b, expected):
        assert math_ops.multiply(a, b) == expected


# --- Division ---

class TestDivide:
    """Tests for the divide method."""

    @pytest.mark.parametrize("a, b, expected", [
        (10, 2, 5.0),
        (7, 2, 3.5),
        (-6, 3, -2.0),
        (0, 5, 0.0),
    ])
    def test_divide(self, math_ops, a, b, expected):
        assert math_ops.divide(a, b) == expected

    def test_divide_by_zero(self, math_ops):
        with pytest.raises(ZeroDivisionError):
            math_ops.divide(10, 0)


# --- Power ---

class TestPower:
    """Tests for the power method."""

    @pytest.mark.parametrize("base, exponent, expected", [
        (2, 3, 8.0),
        (5, 0, 1.0),
        (2, -1, 0.5),
        (10, 2, 100.0),
    ])
    def test_power(self, math_ops, base, exponent, expected):
        assert math_ops.power(base, exponent) == pytest.approx(expected)


# --- Factorial ---

class TestFactorial:
    """Tests for the factorial method."""

    @pytest.mark.parametrize("n, expected", [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial(self, math_ops, n, expected):
        assert math_ops.factorial(n) == expected

    def test_factorial_negative(self, math_ops):
        with pytest.raises(ValueError):
            math_ops.factorial(-1)


# --- Derivative ---

class TestDerivative:
    """Tests for the derivative method."""

    def test_derivative_quadratic(self, math_ops):
        # 3 + 2x + x^2 -> derivative is [2, 2]
        result = math_ops.derivative([3.0, 2.0, 1.0])
        assert result == [2.0, 2.0]

    def test_derivative_cubic(self, math_ops):
        # 1 + 0x + 3x^2 + 4x^3 -> derivative is [0, 6, 12]
        result = math_ops.derivative([1.0, 0.0, 3.0, 4.0])
        assert result == [0.0, 6.0, 12.0]

    def test_derivative_constant(self, math_ops):
        # Constant polynomial -> derivative is [0]
        result = math_ops.derivative([5.0])
        assert result == [0.0]

    def test_derivative_linear(self, math_ops):
        # 2 + 3x -> derivative is [3]
        result = math_ops.derivative([2.0, 3.0])
        assert result == [3.0]


# --- Pi ---

class TestPi:
    """Tests for the pi method."""

    def test_pi_starts_with_3_14(self, math_ops):
        assert math_ops.pi().startswith("3.14159")

    def test_pi_length(self, math_ops):
        # "3." + 40 decimal digits = 42 characters
        assert len(math_ops.pi()) == 42


# --- GCD ---

class TestGcd:
    """Tests for the gcd method."""

    @pytest.mark.parametrize("a, b, expected", [
        (12, 8, 4),
        (100, 75, 25),
        (17, 13, 1),
        (0, 5, 5),
        (-12, 8, 4),
        (54, 24, 6),
    ])
    def test_gcd(self, math_ops, a, b, expected):
        assert math_ops.gcd(a, b) == expected
