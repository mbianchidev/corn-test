"""Unittest (pyunit) tests for MathOperations.

All tests are deterministic and should always pass.
"""

import unittest

from math_operations import MathOperations


class TestAdd(unittest.TestCase):
    """Tests for the add method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_add_positive(self):
        self.assertEqual(self.ops.add(1, 1), 2)

    def test_add_zero(self):
        self.assertEqual(self.ops.add(0, 0), 0)

    def test_add_negative(self):
        self.assertEqual(self.ops.add(-1, -1), -2)

    def test_add_mixed(self):
        self.assertEqual(self.ops.add(-1, 1), 0)

    def test_add_large(self):
        self.assertEqual(self.ops.add(100, 200), 300)


class TestSubtract(unittest.TestCase):
    """Tests for the subtract method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_subtract_positive(self):
        self.assertEqual(self.ops.subtract(5, 3), 2)

    def test_subtract_zero(self):
        self.assertEqual(self.ops.subtract(0, 0), 0)

    def test_subtract_negative(self):
        self.assertEqual(self.ops.subtract(-1, -1), 0)

    def test_subtract_mixed(self):
        self.assertEqual(self.ops.subtract(-1, 1), -2)

    def test_subtract_large(self):
        self.assertEqual(self.ops.subtract(100, 200), -100)


class TestMultiply(unittest.TestCase):
    """Tests for the multiply method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_multiply_positive(self):
        self.assertEqual(self.ops.multiply(2, 3), 6)

    def test_multiply_zero(self):
        self.assertEqual(self.ops.multiply(0, 5), 0)

    def test_multiply_negative(self):
        self.assertEqual(self.ops.multiply(-2, 3), -6)

    def test_multiply_both_negative(self):
        self.assertEqual(self.ops.multiply(-2, -3), 6)

    def test_multiply_large(self):
        self.assertEqual(self.ops.multiply(100, 100), 10000)


class TestDivide(unittest.TestCase):
    """Tests for the divide method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_divide_exact(self):
        self.assertEqual(self.ops.divide(10, 2), 5.0)

    def test_divide_fraction(self):
        self.assertEqual(self.ops.divide(7, 2), 3.5)

    def test_divide_negative(self):
        self.assertEqual(self.ops.divide(-6, 3), -2.0)

    def test_divide_zero_numerator(self):
        self.assertEqual(self.ops.divide(0, 5), 0.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.ops.divide(10, 0)


class TestPower(unittest.TestCase):
    """Tests for the power method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_power_positive(self):
        self.assertAlmostEqual(self.ops.power(2, 3), 8.0)

    def test_power_zero_exponent(self):
        self.assertAlmostEqual(self.ops.power(5, 0), 1.0)

    def test_power_negative_exponent(self):
        self.assertAlmostEqual(self.ops.power(2, -1), 0.5)

    def test_power_large(self):
        self.assertAlmostEqual(self.ops.power(10, 2), 100.0)


class TestFactorial(unittest.TestCase):
    """Tests for the factorial method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_factorial_zero(self):
        self.assertEqual(self.ops.factorial(0), 1)

    def test_factorial_one(self):
        self.assertEqual(self.ops.factorial(1), 1)

    def test_factorial_five(self):
        self.assertEqual(self.ops.factorial(5), 120)

    def test_factorial_ten(self):
        self.assertEqual(self.ops.factorial(10), 3628800)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            self.ops.factorial(-1)


class TestDerivative(unittest.TestCase):
    """Tests for the derivative method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_derivative_quadratic(self):
        self.assertEqual(self.ops.derivative([3.0, 2.0, 1.0]), [2.0, 2.0])

    def test_derivative_cubic(self):
        self.assertEqual(
            self.ops.derivative([1.0, 0.0, 3.0, 4.0]),
            [0.0, 6.0, 12.0],
        )

    def test_derivative_constant(self):
        self.assertEqual(self.ops.derivative([5.0]), [0.0])

    def test_derivative_linear(self):
        self.assertEqual(self.ops.derivative([2.0, 3.0]), [3.0])


class TestPi(unittest.TestCase):
    """Tests for the pi method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_pi_starts_with_3_14(self):
        self.assertTrue(self.ops.pi().startswith("3.14159"))

    def test_pi_length(self):
        self.assertEqual(len(self.ops.pi()), 42)


class TestGcd(unittest.TestCase):
    """Tests for the gcd method."""

    def setUp(self):
        self.ops = MathOperations()

    def test_gcd_basic(self):
        self.assertEqual(self.ops.gcd(12, 8), 4)

    def test_gcd_large(self):
        self.assertEqual(self.ops.gcd(100, 75), 25)

    def test_gcd_coprime(self):
        self.assertEqual(self.ops.gcd(17, 13), 1)

    def test_gcd_zero(self):
        self.assertEqual(self.ops.gcd(0, 5), 5)

    def test_gcd_negative(self):
        self.assertEqual(self.ops.gcd(-12, 8), 4)

    def test_gcd_common(self):
        self.assertEqual(self.ops.gcd(54, 24), 6)


if __name__ == "__main__":
    unittest.main()
