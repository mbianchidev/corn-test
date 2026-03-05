"""unittest tests for MathOperations."""
import unittest
from math_operations import MathOperations


class TestMathOperationsAdd(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_add_positive_numbers(self):
        self.assertEqual(self.math_ops.add(2, 3), 5)
        self.assertEqual(self.math_ops.add(40, 60), 100)

    def test_add_negative_numbers(self):
        self.assertEqual(self.math_ops.add(-2, -3), -5)
        self.assertEqual(self.math_ops.add(5, -5), 0)


class TestMathOperationsSubtract(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_subtract(self):
        self.assertEqual(self.math_ops.subtract(5, 3), 2)
        self.assertEqual(self.math_ops.subtract(3, 5), -2)
        self.assertEqual(self.math_ops.subtract(10, 10), 0)


class TestMathOperationsMultiply(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_multiply(self):
        self.assertEqual(self.math_ops.multiply(2, 3), 6)
        self.assertEqual(self.math_ops.multiply(-2, 3), -6)
        self.assertEqual(self.math_ops.multiply(0, 100), 0)


class TestMathOperationsDivide(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_divide(self):
        self.assertAlmostEqual(self.math_ops.divide(6, 3), 2.0, places=3)
        self.assertAlmostEqual(self.math_ops.divide(5, 2), 2.5, places=3)
        self.assertAlmostEqual(self.math_ops.divide(6, -3), -2.0, places=3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.math_ops.divide(5, 0)


class TestMathOperationsPower(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_power(self):
        self.assertAlmostEqual(self.math_ops.power(2, 3), 8.0, places=3)
        self.assertAlmostEqual(self.math_ops.power(5, 0), 1.0, places=3)
        self.assertAlmostEqual(self.math_ops.power(2, -2), 0.25, places=3)


class TestMathOperationsFactorial(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_factorial(self):
        self.assertEqual(self.math_ops.factorial(0), 1)
        self.assertEqual(self.math_ops.factorial(1), 1)
        self.assertEqual(self.math_ops.factorial(2), 2)
        self.assertEqual(self.math_ops.factorial(3), 6)
        self.assertEqual(self.math_ops.factorial(4), 24)
        self.assertEqual(self.math_ops.factorial(5), 120)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            self.math_ops.factorial(-1)


class TestMathOperationsPi(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_pi(self):
        self.assertEqual(
            self.math_ops.pi(),
            "3.1415926535897932384626433832795028841971",
        )


class TestMathOperationsGcd(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_gcd(self):
        self.assertEqual(self.math_ops.gcd(1, 1), 1)
        self.assertEqual(self.math_ops.gcd(10, 15), 5)
        self.assertEqual(self.math_ops.gcd(48, 18), 6)
        self.assertEqual(self.math_ops.gcd(17, 19), 1)

    def test_gcd_negative(self):
        self.assertEqual(self.math_ops.gcd(-10, 15), 5)
        self.assertEqual(self.math_ops.gcd(48, -18), 6)
        self.assertEqual(self.math_ops.gcd(-14, -21), 7)


class TestMathOperationsDerivative(unittest.TestCase):
    def setUp(self):
        self.math_ops = MathOperations()

    def test_derivative(self):
        self.assertEqual(self.math_ops.derivative([3, 2, 5]), [2, 10])
        self.assertEqual(self.math_ops.derivative([0, 0, 0, 1]), [0, 0, 3])
        self.assertEqual(self.math_ops.derivative([7]), [0.0])

    def test_derivative_empty(self):
        self.assertEqual(self.math_ops.derivative([]), [0.0])

    def test_derivative_none(self):
        with self.assertRaises(ValueError):
            self.math_ops.derivative(None)


if __name__ == "__main__":
    unittest.main()
