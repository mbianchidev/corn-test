import 'dart:math';

/// Deterministic mathematical operations.
class MathOperations {
  /// Adds two integers.
  int add(int a, int b) => a + b;

  /// Subtracts two integers.
  int subtract(int a, int b) => a - b;

  /// Multiplies two integers.
  int multiply(int a, int b) => a * b;

  /// Divides two numbers. Throws [ArgumentError] if divisor is zero.
  double divide(int a, int b) {
    if (b == 0) throw ArgumentError('Division by zero');
    return a / b;
  }

  /// Calculates the power of a number.
  double power(double base, int exponent) => pow(base, exponent).toDouble();

  /// Calculates the factorial. Throws [ArgumentError] for negative numbers.
  int factorial(int n) {
    if (n < 0) throw ArgumentError('Factorial is not defined for negative numbers');
    if (n <= 1) return 1;
    var result = 1;
    for (var i = 2; i <= n; i++) {
      result *= i;
    }
    return result;
  }

  /// Computes the derivative of a polynomial represented by coefficients.
  List<double> derivative(List<double> coefficients) {
    if (coefficients.length <= 1) return [0.0];
    return List.generate(
      coefficients.length - 1,
      (i) => coefficients[i + 1] * (i + 1),
    );
  }

  /// Returns the first 40 decimals of pi.
  String pi() => '3.1415926535897932384626433832795028841971';

  /// Calculates the greatest common divisor using Euclidean algorithm.
  int gcd(int a, int b) {
    a = a.abs();
    b = b.abs();
    while (b != 0) {
      final temp = b;
      b = a % b;
      a = temp;
    }
    return a;
  }
}
