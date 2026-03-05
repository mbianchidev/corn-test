"""unittest tests for RandomMathOperations - intentionally flaky."""
import unittest
from random_math_operations import RandomMathOperations


class TestRandomOddNumber(unittest.TestCase):
    def setUp(self):
        self.random_ops = RandomMathOperations()

    def _test_odd(self):
        number = self.random_ops.generate_random_odd_number()
        self.assertGreaterEqual(number, 1, f"Number should be >= 1, got {number}")
        self.assertLessEqual(number, 100, f"Number should be <= 100, got {number}")
        self.assertEqual(number % 2, 1, f"Number should be odd, got {number}")


# Generate 20 test methods for repeated runs
for i in range(1, 21):
    def make_test(run_num):
        def test_method(self):
            self._test_odd()
        test_method.__doc__ = f"Run {run_num}/20: random odd number should be odd"
        return test_method
    setattr(TestRandomOddNumber, f"test_run_{i:02d}_odd", make_test(i))


class TestRandomEvenNumber(unittest.TestCase):
    def setUp(self):
        self.random_ops = RandomMathOperations()

    def _test_even(self):
        number = self.random_ops.generate_random_even_number()
        self.assertGreaterEqual(number, 0, f"Number should be >= 0, got {number}")
        self.assertLessEqual(number, 100, f"Number should be <= 100, got {number}")
        self.assertEqual(number % 2, 0, f"Number should be even, got {number}")


for i in range(1, 21):
    def make_test(run_num):
        def test_method(self):
            self._test_even()
        test_method.__doc__ = f"Run {run_num}/20: random even number should be even"
        return test_method
    setattr(TestRandomEvenNumber, f"test_run_{i:02d}_even", make_test(i))


class TestRandomPrimeCandidate(unittest.TestCase):
    def setUp(self):
        self.random_ops = RandomMathOperations()

    def _test_prime(self):
        number = self.random_ops.generate_random_prime_candidate()
        self.assertGreaterEqual(number, 2, f"Number should be >= 2, got {number}")
        self.assertLessEqual(number, 200, f"Number should be <= 200, got {number}")
        self.assertTrue(
            RandomMathOperations.is_prime(number),
            f"Number should be prime, got {number}",
        )


for i in range(1, 21):
    def make_test(run_num):
        def test_method(self):
            self._test_prime()
        test_method.__doc__ = f"Run {run_num}/20: random prime candidate should be prime"
        return test_method
    setattr(TestRandomPrimeCandidate, f"test_run_{i:02d}_prime", make_test(i))


class TestIsPrime(unittest.TestCase):
    def test_prime_numbers(self):
        self.assertTrue(RandomMathOperations.is_prime(2))
        self.assertTrue(RandomMathOperations.is_prime(3))
        self.assertTrue(RandomMathOperations.is_prime(5))
        self.assertTrue(RandomMathOperations.is_prime(7))
        self.assertTrue(RandomMathOperations.is_prime(11))
        self.assertTrue(RandomMathOperations.is_prime(97))

    def test_non_prime_numbers(self):
        self.assertFalse(RandomMathOperations.is_prime(1))
        self.assertFalse(RandomMathOperations.is_prime(4))
        self.assertFalse(RandomMathOperations.is_prime(6))
        self.assertFalse(RandomMathOperations.is_prime(9))
        self.assertFalse(RandomMathOperations.is_prime(100))


if __name__ == "__main__":
    unittest.main()
