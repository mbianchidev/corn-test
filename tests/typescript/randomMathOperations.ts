/**
 * Class containing random mathematical operations.
 * Some methods have intentional flaws to produce flaky test results.
 */
export class RandomMathOperations {
  /**
   * Generates a random odd number between 1 and 99.
   */
  generateRandomOddNumber(): number {
    const number = Math.floor(Math.random() * 50) * 2 + 1;
    return number;
  }

  /**
   * Generates a random even number between 0 and 100.
   * Intentional flaw: 5% of the time, adds 1 to make it odd.
   */
  generateRandomEvenNumber(): number {
    let number = Math.floor(Math.random() * 51) * 2;

    // Intentional flaw: 5% of the time, add 1 to make it odd
    if (Math.random() < 0.05) {
      number += 1;
    }

    return number;
  }

  /**
   * Generates a random prime candidate between 2 and 97.
   */
  generateRandomPrimeCandidate(): number {
    const primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97];
    const primeIndex = Math.floor(Math.random() * primes.length);
    return primes[primeIndex];
  }

  /**
   * Helper method to check if a number is prime.
   */
  static isPrime(n: number): boolean {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 === 0 || n % 3 === 0) return false;

    for (let i = 5; i * i <= n; i += 6) {
      if (n % i === 0 || n % (i + 2) === 0) {
        return false;
      }
    }
    return true;
  }
}
