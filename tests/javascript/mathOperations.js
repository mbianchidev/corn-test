/**
 * Class containing deterministic mathematical operations.
 */
class MathOperations {
  /**
   * Adds two integers.
   */
  add(a, b) {
    return a + b;
  }

  /**
   * Subtracts two integers.
   */
  subtract(a, b) {
    return a - b;
  }

  /**
   * Multiplies two integers.
   */
  multiply(a, b) {
    return a * b;
  }

  /**
   * Divides two numbers.
   * @throws {Error} if divisor is zero
   */
  divide(a, b) {
    if (b === 0) {
      throw new Error("Division by zero");
    }
    return a / b;
  }

  /**
   * Calculates the power of a number.
   */
  power(base, exponent) {
    return Math.pow(base, exponent);
  }

  /**
   * Calculates the factorial of a number.
   * @throws {Error} if n is negative
   */
  factorial(n) {
    if (n < 0) {
      throw new Error("Factorial is not defined for negative numbers");
    }
    if (n === 0 || n === 1) {
      return 1;
    }
    let result = 1;
    for (let i = 2; i <= n; i++) {
      result *= i;
    }
    return result;
  }

  /**
   * Computes the derivative of a polynomial represented by its coefficients.
   * coefficients[0] + coefficients[1]*x + coefficients[2]*x^2 + ...
   */
  derivative(coefficients) {
    if (coefficients === null || coefficients === undefined) {
      throw new Error("Coefficients array must not be null");
    }
    if (coefficients.length <= 1) {
      return [0];
    }
    const result = [];
    for (let i = 1; i < coefficients.length; i++) {
      result.push(coefficients[i] * i);
    }
    return result;
  }

  /**
   * Returns the first 40 decimals of the pi constant.
   */
  pi() {
    return "3.1415926535897932384626433832795028841971";
  }

  /**
   * Calculates the greatest common divisor using Euclidean algorithm.
   */
  gcd(a, b) {
    a = Math.abs(a);
    b = Math.abs(b);
    while (b !== 0) {
      const temp = b;
      b = a % b;
      a = temp;
    }
    return a;
  }
}

module.exports = { MathOperations };
