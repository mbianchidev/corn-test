/**
 * Class containing deterministic mathematical operations.
 */
export class MathOperations {
  /**
   * Adds two numbers.
   */
  add(a: number, b: number): number {
    return a + b;
  }

  /**
   * Subtracts two numbers.
   */
  subtract(a: number, b: number): number {
    return a - b;
  }

  /**
   * Multiplies two numbers.
   */
  multiply(a: number, b: number): number {
    return a * b;
  }

  /**
   * Divides two numbers.
   * @throws Error if divisor is zero
   */
  divide(a: number, b: number): number {
    if (b === 0) {
      throw new Error("Division by zero");
    }
    return a / b;
  }

  /**
   * Calculates the power of a number.
   */
  power(base: number, exponent: number): number {
    return Math.pow(base, exponent);
  }

  /**
   * Calculates the factorial of a number.
   * @throws Error if n is negative
   */
  factorial(n: number): number {
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
   * The coefficients array represents the polynomial:
   *   coefficients[0] + coefficients[1]*x + coefficients[2]*x^2 + ... + coefficients[n]*x^n
   *
   * @param coefficients the polynomial coefficients in ascending order of degree
   * @returns the coefficients of the derivative polynomial
   * @throws Error if coefficients is null or undefined
   */
  derivative(coefficients: number[]): number[] {
    if (coefficients == null) {
      throw new Error("Coefficients array must not be null");
    }
    if (coefficients.length <= 1) {
      return [0];
    }
    const result: number[] = new Array(coefficients.length - 1);
    for (let i = 1; i < coefficients.length; i++) {
      result[i - 1] = coefficients[i] * i;
    }
    return result;
  }

  /**
   * Returns the first 40 decimals of the pi constant π.
   */
  pi(): string {
    return "3.1415926535897932384626433832795028841971";
  }

  /**
   * Calculates the greatest common divisor of two numbers using Euclidean algorithm.
   */
  gcd(a: number, b: number): number {
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
