import 'package:test/test.dart';
import 'package:corn_test_dart/random_math_operations.dart';

void main() {
  late RandomMathOperations randomOps;

  setUp(() {
    randomOps = RandomMathOperations();
  });

  group('generateRandomOddNumber', () {
    for (var i = 1; i <= 20; i++) {
      test('iteration $i: should generate an odd number', () {
        final number = randomOps.generateRandomOddNumber();
        expect(number, greaterThanOrEqualTo(1));
        expect(number, lessThanOrEqualTo(99));
        expect(number % 2, equals(1), reason: 'Number should be odd, got: $number');
      });
    }
  });

  group('generateRandomEvenNumber (Flaky: 5% failure rate)', () {
    for (var i = 1; i <= 20; i++) {
      test('iteration $i: should generate an even number', () {
        final number = randomOps.generateRandomEvenNumber();
        expect(number, greaterThanOrEqualTo(0));
        expect(number, lessThanOrEqualTo(101));
        expect(number % 2, equals(0), reason: 'Number should be even, got: $number');
      });
    }
  });

  group('generateRandomPrimeCandidate', () {
    for (var i = 1; i <= 20; i++) {
      test('iteration $i: should generate a prime number', () {
        final number = randomOps.generateRandomPrimeCandidate();
        expect(number, greaterThanOrEqualTo(2));
        expect(number, lessThanOrEqualTo(97));
        expect(RandomMathOperations.isPrime(number), isTrue,
            reason: 'Number should be prime, got: $number');
      });
    }
  });

  group('isPrime', () {
    test('correctly identifies prime numbers', () {
      expect(RandomMathOperations.isPrime(2), isTrue);
      expect(RandomMathOperations.isPrime(3), isTrue);
      expect(RandomMathOperations.isPrime(5), isTrue);
      expect(RandomMathOperations.isPrime(97), isTrue);
    });

    test('correctly identifies non-prime numbers', () {
      expect(RandomMathOperations.isPrime(1), isFalse);
      expect(RandomMathOperations.isPrime(4), isFalse);
      expect(RandomMathOperations.isPrime(100), isFalse);
    });
  });
}
