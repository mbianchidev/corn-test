import { test, expect } from '@playwright/test';
import { MathOperations } from '../../src/mathOperations';

/**
 * Playwright test suite for MathOperations.
 * These tests are deterministic and should always pass.
 * Tests import source directly (no browser app needed).
 */
test.describe('MathOperations Tests', () => {
  let mathOps: MathOperations;

  test.beforeEach(() => {
    mathOps = new MathOperations();
  });

  test('Addition should correctly add two positive numbers', () => {
    expect(mathOps.add(2, 3)).toBe(5);
    expect(mathOps.add(40, 60)).toBe(100);
  });

  test('Addition should correctly handle negative numbers', () => {
    expect(mathOps.add(-2, -3)).toBe(-5);
    expect(mathOps.add(5, -5)).toBe(0);
  });

  test('Subtraction should correctly subtract two numbers', () => {
    expect(mathOps.subtract(5, 3)).toBe(2);
    expect(mathOps.subtract(3, 5)).toBe(-2);
    expect(mathOps.subtract(10, 10)).toBe(0);
  });

  test('Multiplication should correctly multiply two numbers', () => {
    expect(mathOps.multiply(2, 3)).toBe(6);
    expect(mathOps.multiply(-2, 3)).toBe(-6);
    expect(mathOps.multiply(0, 100)).toBe(0);
  });

  test('Division should correctly divide two numbers', () => {
    expect(mathOps.divide(6, 3)).toBeCloseTo(2.0, 3);
    expect(mathOps.divide(5, 2)).toBeCloseTo(2.5, 3);
    expect(mathOps.divide(6, -3)).toBeCloseTo(-2.0, 3);
  });

  test('Division by zero should throw Error', () => {
    expect(() => mathOps.divide(5, 0)).toThrow('Division by zero');
  });

  test('Power should correctly calculate exponentials', () => {
    expect(mathOps.power(2, 3)).toBeCloseTo(8.0, 3);
    expect(mathOps.power(5, 0)).toBeCloseTo(1.0, 3);
    expect(mathOps.power(2, -2)).toBeCloseTo(0.25, 3);
  });

  test('Factorial should correctly calculate factorials', () => {
    expect(mathOps.factorial(0)).toBe(1);
    expect(mathOps.factorial(1)).toBe(1);
    expect(mathOps.factorial(2)).toBe(2);
    expect(mathOps.factorial(3)).toBe(6);
    expect(mathOps.factorial(4)).toBe(24);
    expect(mathOps.factorial(5)).toBe(120);
  });

  test('Factorial with negative number should throw Error', () => {
    expect(() => mathOps.factorial(-1)).toThrow('Factorial is not defined for negative numbers');
  });

  test('Pi should return the first 40 decimals of pi', () => {
    expect(mathOps.pi()).toBe('3.1415926535897932384626433832795028841971');
  });

  test('GCD should correctly calculate greatest common divisor', () => {
    expect(mathOps.gcd(1, 1)).toBe(1);
    expect(mathOps.gcd(10, 15)).toBe(5);
    expect(mathOps.gcd(48, 18)).toBe(6);
    expect(mathOps.gcd(17, 19)).toBe(1);
  });

  test('GCD should handle negative numbers', () => {
    expect(mathOps.gcd(-10, 15)).toBe(5);
    expect(mathOps.gcd(48, -18)).toBe(6);
    expect(mathOps.gcd(-14, -21)).toBe(7);
  });

  test('Derivative of a polynomial should return correct coefficients', () => {
    expect(mathOps.derivative([3, 2, 5])).toEqual([2, 10]);
    expect(mathOps.derivative([0, 0, 0, 1])).toEqual([0, 0, 3]);
    expect(mathOps.derivative([7])).toEqual([0]);
  });

  test('Derivative of empty polynomial should return zero', () => {
    expect(mathOps.derivative([])).toEqual([0]);
  });

  test('Derivative with null coefficients should throw Error', () => {
    expect(() => mathOps.derivative(null as unknown as number[])).toThrow(
      'Coefficients array must not be null'
    );
  });
});
