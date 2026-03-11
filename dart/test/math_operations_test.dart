import 'package:test/test.dart';
import 'package:corn_test_dart/math_operations.dart';

void main() {
  late MathOperations mathOps;

  setUp(() {
    mathOps = MathOperations();
  });

  group('add', () {
    test('adds positive numbers', () {
      expect(mathOps.add(2, 3), equals(5));
      expect(mathOps.add(40, 60), equals(100));
    });

    test('adds negative numbers', () {
      expect(mathOps.add(-2, -3), equals(-5));
      expect(mathOps.add(5, -5), equals(0));
    });
  });

  group('subtract', () {
    test('subtracts two numbers', () {
      expect(mathOps.subtract(5, 3), equals(2));
      expect(mathOps.subtract(3, 5), equals(-2));
    });
  });

  group('multiply', () {
    test('multiplies two numbers', () {
      expect(mathOps.multiply(2, 3), equals(6));
      expect(mathOps.multiply(-2, 3), equals(-6));
      expect(mathOps.multiply(0, 100), equals(0));
    });
  });

  group('divide', () {
    test('divides two numbers', () {
      expect(mathOps.divide(6, 3), closeTo(2.0, 0.001));
      expect(mathOps.divide(5, 2), closeTo(2.5, 0.001));
    });

    test('throws on division by zero', () {
      expect(() => mathOps.divide(5, 0), throwsArgumentError);
    });
  });

  group('power', () {
    test('calculates power', () {
      expect(mathOps.power(2, 3), closeTo(8.0, 0.001));
      expect(mathOps.power(5, 0), closeTo(1.0, 0.001));
    });
  });

  group('factorial', () {
    test('calculates factorial', () {
      expect(mathOps.factorial(0), equals(1));
      expect(mathOps.factorial(1), equals(1));
      expect(mathOps.factorial(5), equals(120));
    });

    test('throws for negative numbers', () {
      expect(() => mathOps.factorial(-1), throwsArgumentError);
    });
  });

  group('derivative', () {
    test('calculates polynomial derivative', () {
      expect(mathOps.derivative([3, 2, 5]), orderedEquals([2.0, 10.0]));
      expect(mathOps.derivative([7]), orderedEquals([0.0]));
      expect(mathOps.derivative([]), orderedEquals([0.0]));
    });
  });

  group('pi', () {
    test('returns first 40 decimals of pi', () {
      expect(mathOps.pi(), equals('3.1415926535897932384626433832795028841971'));
    });
  });

  group('gcd', () {
    test('calculates greatest common divisor', () {
      expect(mathOps.gcd(10, 15), equals(5));
      expect(mathOps.gcd(48, 18), equals(6));
      expect(mathOps.gcd(17, 19), equals(1));
    });

    test('handles negative numbers', () {
      expect(mathOps.gcd(-10, 15), equals(5));
      expect(mathOps.gcd(48, -18), equals(6));
    });
  });
}
