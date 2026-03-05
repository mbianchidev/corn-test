"""pytest tests for MathOperations."""
import pytest
from math_operations import MathOperations


@pytest.fixture
def math_ops():
    return MathOperations()


class TestMathOperationsAdd:
    def test_add_positive_numbers(self, math_ops):
        assert math_ops.add(2, 3) == 5
        assert math_ops.add(40, 60) == 100

    def test_add_negative_numbers(self, math_ops):
        assert math_ops.add(-2, -3) == -5
        assert math_ops.add(5, -5) == 0


class TestMathOperationsSubtract:
    def test_subtract(self, math_ops):
        assert math_ops.subtract(5, 3) == 2
        assert math_ops.subtract(3, 5) == -2
        assert math_ops.subtract(10, 10) == 0


class TestMathOperationsMultiply:
    def test_multiply(self, math_ops):
        assert math_ops.multiply(2, 3) == 6
        assert math_ops.multiply(-2, 3) == -6
        assert math_ops.multiply(0, 100) == 0


class TestMathOperationsDivide:
    def test_divide(self, math_ops):
        assert math_ops.divide(6, 3) == pytest.approx(2.0, abs=0.001)
        assert math_ops.divide(5, 2) == pytest.approx(2.5, abs=0.001)
        assert math_ops.divide(6, -3) == pytest.approx(-2.0, abs=0.001)

    def test_divide_by_zero(self, math_ops):
        with pytest.raises(ZeroDivisionError):
            math_ops.divide(5, 0)


class TestMathOperationsPower:
    def test_power(self, math_ops):
        assert math_ops.power(2, 3) == pytest.approx(8.0, abs=0.001)
        assert math_ops.power(5, 0) == pytest.approx(1.0, abs=0.001)
        assert math_ops.power(2, -2) == pytest.approx(0.25, abs=0.001)


class TestMathOperationsFactorial:
    def test_factorial(self, math_ops):
        assert math_ops.factorial(0) == 1
        assert math_ops.factorial(1) == 1
        assert math_ops.factorial(2) == 2
        assert math_ops.factorial(3) == 6
        assert math_ops.factorial(4) == 24
        assert math_ops.factorial(5) == 120

    def test_factorial_negative(self, math_ops):
        with pytest.raises(ValueError):
            math_ops.factorial(-1)


class TestMathOperationsPi:
    def test_pi(self, math_ops):
        assert math_ops.pi() == "3.1415926535897932384626433832795028841971"


class TestMathOperationsGcd:
    def test_gcd(self, math_ops):
        assert math_ops.gcd(1, 1) == 1
        assert math_ops.gcd(10, 15) == 5
        assert math_ops.gcd(48, 18) == 6
        assert math_ops.gcd(17, 19) == 1

    def test_gcd_negative(self, math_ops):
        assert math_ops.gcd(-10, 15) == 5
        assert math_ops.gcd(48, -18) == 6
        assert math_ops.gcd(-14, -21) == 7


class TestMathOperationsDerivative:
    def test_derivative(self, math_ops):
        assert math_ops.derivative([3, 2, 5]) == [2, 10]
        assert math_ops.derivative([0, 0, 0, 1]) == [0, 0, 3]
        assert math_ops.derivative([7]) == [0.0]

    def test_derivative_empty(self, math_ops):
        assert math_ops.derivative([]) == [0.0]

    def test_derivative_none(self, math_ops):
        with pytest.raises(ValueError):
            math_ops.derivative(None)
