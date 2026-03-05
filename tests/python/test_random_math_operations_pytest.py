"""pytest tests for RandomMathOperations - intentionally flaky."""
import pytest
from random_math_operations import RandomMathOperations


@pytest.fixture
def random_ops():
    return RandomMathOperations()


class TestRandomOddNumber:
    @pytest.mark.parametrize("run", range(1, 21))
    def test_random_odd_number_should_be_odd(self, random_ops, run):
        number = random_ops.generate_random_odd_number()
        assert 1 <= number <= 100, f"Number should be between 1 and 100, got {number}"
        assert number % 2 == 1, f"Number should be odd, got {number}"


class TestRandomEvenNumber:
    @pytest.mark.parametrize("run", range(1, 21))
    def test_random_even_number_should_be_even(self, random_ops, run):
        number = random_ops.generate_random_even_number()
        assert 0 <= number <= 100, f"Number should be between 0 and 100, got {number}"
        assert number % 2 == 0, f"Number should be even, got {number}"


class TestRandomPrimeCandidate:
    @pytest.mark.parametrize("run", range(1, 21))
    def test_random_prime_candidate_should_be_prime(self, random_ops, run):
        number = random_ops.generate_random_prime_candidate()
        assert 2 <= number <= 200, f"Number should be between 2 and 200, got {number}"
        assert RandomMathOperations.is_prime(number), f"Number should be prime, got {number}"


class TestIsPrime:
    def test_prime_numbers(self):
        assert RandomMathOperations.is_prime(2) is True
        assert RandomMathOperations.is_prime(3) is True
        assert RandomMathOperations.is_prime(5) is True
        assert RandomMathOperations.is_prime(7) is True
        assert RandomMathOperations.is_prime(11) is True
        assert RandomMathOperations.is_prime(97) is True

    def test_non_prime_numbers(self):
        assert RandomMathOperations.is_prime(1) is False
        assert RandomMathOperations.is_prime(4) is False
        assert RandomMathOperations.is_prime(6) is False
        assert RandomMathOperations.is_prime(9) is False
        assert RandomMathOperations.is_prime(100) is False
