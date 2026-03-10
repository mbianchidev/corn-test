"""Pytest flaky tests for RandomMathOperations.

These tests exercise random number generators that contain intentional
flaws, causing intermittent test failures. Each test is run 20 times
via parametrize to surface the flaky behavior.
"""

import pytest

from random_math_operations import RandomMathOperations


@pytest.fixture
def rng():
    """Provide a RandomMathOperations instance (no fixed seed)."""
    return RandomMathOperations()


class TestGenerateRandomOddNumber:
    """Tests for generate_random_odd_number — always reliable."""

    @pytest.mark.parametrize("iteration", range(20))
    def test_odd_number_is_odd(self, rng, iteration):
        value = rng.generate_random_odd_number()
        assert value % 2 == 1, f"Expected odd, got {value}"

    @pytest.mark.parametrize("iteration", range(20))
    def test_odd_number_in_range(self, rng, iteration):
        value = rng.generate_random_odd_number()
        assert 1 <= value <= 99, f"Expected 1-99, got {value}"


class TestGenerateRandomEvenNumber:
    """Tests for generate_random_even_number — flaky due to 5% flaw."""

    @pytest.mark.parametrize("iteration", range(20))
    def test_even_number_is_even(self, rng, iteration):
        value = rng.generate_random_even_number()
        assert value % 2 == 0, f"Expected even, got {value}"

    @pytest.mark.parametrize("iteration", range(20))
    def test_even_number_in_range(self, rng, iteration):
        value = rng.generate_random_even_number()
        assert 0 <= value <= 100, f"Expected 0-100, got {value}"


class TestGenerateRandomPrimeCandidate:
    """Tests for generate_random_prime_candidate — always reliable."""

    @pytest.mark.parametrize("iteration", range(20))
    def test_prime_candidate_is_prime(self, rng, iteration):
        value = rng.generate_random_prime_candidate()
        assert RandomMathOperations.is_prime(value), \
            f"Expected prime, got {value}"

    @pytest.mark.parametrize("iteration", range(20))
    def test_prime_candidate_in_range(self, rng, iteration):
        value = rng.generate_random_prime_candidate()
        assert 2 <= value <= 97, f"Expected 2-97, got {value}"


class TestIsPrime:
    """Deterministic tests for the is_prime static helper."""

    @pytest.mark.parametrize("n, expected", [
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (18, False),
        (97, True),
        (1, False),
        (0, False),
        (-5, False),
    ])
    def test_is_prime(self, n, expected):
        assert RandomMathOperations.is_prime(n) == expected
