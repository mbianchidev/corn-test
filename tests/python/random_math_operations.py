"""
Module containing random mathematical operations.
Some methods have intentional flaws to produce flaky test results.
"""
import random


class RandomMathOperations:
    """Class containing random mathematical operations."""

    def generate_random_odd_number(self) -> int:
        """Generates a random odd number between 1 and 99."""
        number = random.randint(0, 49) * 2 + 1
        return number

    def generate_random_even_number(self) -> int:
        """
        Generates a random even number between 0 and 100.
        Intentional flaw: 5% of the time, adds 1 to make it odd.
        """
        number = random.randint(0, 50) * 2

        # Intentional flaw: 5% of the time, add 1 to make it odd
        if random.random() < 0.05:
            number += 1

        return number

    def generate_random_prime_candidate(self) -> int:
        """Generates a random prime candidate between 2 and 97."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        return random.choice(primes)

    @staticmethod
    def is_prime(n: int) -> bool:
        """Helper method to check if a number is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
