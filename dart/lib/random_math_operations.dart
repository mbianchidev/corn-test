import 'dart:math';

/// Random mathematical operations with intentional flakiness.
class RandomMathOperations {
  final Random _random;

  RandomMathOperations([int? seed]) : _random = Random(seed);

  /// Generates a random odd number between 1 and 99.
  int generateRandomOddNumber() {
    return _random.nextInt(50) * 2 + 1;
  }

  /// Generates a random even number between 0 and 100.
  /// Intentional flaw: 5% of the time adds 1 to make it odd.
  int generateRandomEvenNumber() {
    var number = _random.nextInt(51) * 2;
    if (_random.nextDouble() < 0.05) {
      number += 1;
    }
    return number;
  }

  /// Generates a random prime candidate from a list of primes 2-97.
  int generateRandomPrimeCandidate() {
    const primes = [
      2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
      53, 59, 61, 67, 71, 73, 79, 83, 89, 97
    ];
    return primes[_random.nextInt(primes.length)];
  }

  /// Checks if a number is prime.
  static bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (var i = 5; i * i <= n; i += 6) {
      if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
  }
}
