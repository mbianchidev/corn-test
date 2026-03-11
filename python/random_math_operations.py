"""Random mathematical operations module with intentional flaky behavior.

This module provides a RandomMathOperations class that generates random
numbers with certain mathematical properties. Some methods contain
intentional flaws that cause intermittent failures in tests.
"""

import random


# Primes between 2 and 97
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


class RandomMathOperations:
    """Random number generation with mathematical properties.

    Some methods contain intentional flaws that produce incorrect
    results a small percentage of the time, making tests flaky.
    """

    def __init__(self, seed: int | None = None):
        """Initialize with an optional random seed.

        Args:
            seed: Optional seed for reproducibility.
        """
        self._rng = random.Random(seed)

    def generate_random_odd_number(self) -> int:
        """Generate a random odd number between 1 and 99.

        This method is reliable and always returns a valid odd number.

        Returns:
            A random odd integer in [1, 99].
        """
        return self._rng.randrange(1, 100, 2)

    def generate_random_even_number(self) -> int:
        """Generate a random even number between 0 and 100.

        **Intentional flaw**: 5% of the time, adds 1 to the result,
        making it odd instead of even.

        Returns:
            A random even integer in [0, 100], but occasionally an odd
            number due to the intentional flaw.
        """
        value = self._rng.randrange(0, 101, 2)
        # Intentional flaw: 5% chance of corrupting the result
        if self._rng.random() < 0.05:
            value += 1
        return value

    def generate_random_prime_candidate(self) -> int:
        """Return a random prime number from a list of known primes (2-97).

        This method is reliable and always returns a valid prime.

        Returns:
            A random prime number from the predefined list.
        """
        return self._rng.choice(PRIMES)

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime using trial division.

        Args:
            n: The integer to test.

        Returns:
            True if n is prime, False otherwise.
        """
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
