"""Unittest (pyunit) flaky tests for RandomMathOperations.

These tests exercise random number generators that contain intentional
flaws, causing intermittent test failures. Each flaky test is run
20 times via subTest to surface the flaky behavior.
"""

import unittest

from random_math_operations import RandomMathOperations


class TestGenerateRandomOddNumber(unittest.TestCase):
    """Tests for generate_random_odd_number — always reliable."""

    def setUp(self):
        self.rng = RandomMathOperations()

    def test_odd_number_is_odd(self):
        for i in range(20):
            with self.subTest(iteration=i):
                value = self.rng.generate_random_odd_number()
                self.assertEqual(value % 2, 1, f"Expected odd, got {value}")

    def test_odd_number_in_range(self):
        for i in range(20):
            with self.subTest(iteration=i):
                value = self.rng.generate_random_odd_number()
                self.assertGreaterEqual(value, 1)
                self.assertLessEqual(value, 99)


class TestGenerateRandomEvenNumber(unittest.TestCase):
    """Tests for generate_random_even_number — flaky due to 5% flaw."""

    def setUp(self):
        self.rng = RandomMathOperations()

    def test_even_number_is_even(self):
        for i in range(20):
            with self.subTest(iteration=i):
                value = self.rng.generate_random_even_number()
                self.assertEqual(
                    value % 2, 0, f"Expected even, got {value}"
                )

    def test_even_number_in_range(self):
        for i in range(20):
            with self.subTest(iteration=i):
                value = self.rng.generate_random_even_number()
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 100)


class TestGenerateRandomPrimeCandidate(unittest.TestCase):
    """Tests for generate_random_prime_candidate — always reliable."""

    def setUp(self):
        self.rng = RandomMathOperations()

    def test_prime_candidate_is_prime(self):
        for i in range(20):
            with self.subTest(iteration=i):
                value = self.rng.generate_random_prime_candidate()
                self.assertTrue(
                    RandomMathOperations.is_prime(value),
                    f"Expected prime, got {value}",
                )

    def test_prime_candidate_in_range(self):
        for i in range(20):
            with self.subTest(iteration=i):
                value = self.rng.generate_random_prime_candidate()
                self.assertGreaterEqual(value, 2)
                self.assertLessEqual(value, 97)


class TestIsPrime(unittest.TestCase):
    """Deterministic tests for the is_prime static helper."""

    def test_prime_two(self):
        self.assertTrue(RandomMathOperations.is_prime(2))

    def test_prime_three(self):
        self.assertTrue(RandomMathOperations.is_prime(3))

    def test_not_prime_four(self):
        self.assertFalse(RandomMathOperations.is_prime(4))

    def test_prime_seventeen(self):
        self.assertTrue(RandomMathOperations.is_prime(17))

    def test_not_prime_eighteen(self):
        self.assertFalse(RandomMathOperations.is_prime(18))

    def test_prime_ninety_seven(self):
        self.assertTrue(RandomMathOperations.is_prime(97))

    def test_not_prime_one(self):
        self.assertFalse(RandomMathOperations.is_prime(1))

    def test_not_prime_zero(self):
        self.assertFalse(RandomMathOperations.is_prime(0))

    def test_not_prime_negative(self):
        self.assertFalse(RandomMathOperations.is_prime(-5))


if __name__ == "__main__":
    unittest.main()
