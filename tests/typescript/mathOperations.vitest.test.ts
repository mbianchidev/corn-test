import { describe, it, expect, beforeEach } from 'vitest';
import { MathOperations } from './mathOperations';

describe('MathOperations (Vitest)', () => {
  let mathOps: MathOperations;

  beforeEach(() => {
    mathOps = new MathOperations();
  });

  describe('add', () => {
    it('should correctly add two positive numbers', () => {
      expect(mathOps.add(2, 3)).toBe(5);
      expect(mathOps.add(40, 60)).toBe(100);
    });

    it('should correctly handle negative numbers', () => {
      expect(mathOps.add(-2, -3)).toBe(-5);
      expect(mathOps.add(5, -5)).toBe(0);
    });
  });

  describe('subtract', () => {
    it('should correctly subtract two numbers', () => {
      expect(mathOps.subtract(5, 3)).toBe(2);
      expect(mathOps.subtract(3, 5)).toBe(-2);
      expect(mathOps.subtract(10, 10)).toBe(0);
    });
  });

  describe('multiply', () => {
    it('should correctly multiply two numbers', () => {
      expect(mathOps.multiply(2, 3)).toBe(6);
      expect(mathOps.multiply(-2, 3)).toBe(-6);
      expect(mathOps.multiply(0, 100)).toBe(0);
    });
  });

  describe('divide', () => {
    it('should correctly divide two numbers', () => {
      expect(mathOps.divide(6, 3)).toBeCloseTo(2.0, 3);
      expect(mathOps.divide(5, 2)).toBeCloseTo(2.5, 3);
      expect(mathOps.divide(6, -3)).toBeCloseTo(-2.0, 3);
    });

    it('should throw on division by zero', () => {
      expect(() => mathOps.divide(5, 0)).toThrow('Division by zero');
    });
  });

  describe('power', () => {
    it('should correctly calculate exponentials', () => {
      expect(mathOps.power(2, 3)).toBeCloseTo(8.0, 3);
      expect(mathOps.power(5, 0)).toBeCloseTo(1.0, 3);
      expect(mathOps.power(2, -2)).toBeCloseTo(0.25, 3);
    });
  });

  describe('factorial', () => {
    it('should correctly calculate factorials', () => {
      expect(mathOps.factorial(0)).toBe(1);
      expect(mathOps.factorial(1)).toBe(1);
      expect(mathOps.factorial(2)).toBe(2);
      expect(mathOps.factorial(3)).toBe(6);
      expect(mathOps.factorial(4)).toBe(24);
      expect(mathOps.factorial(5)).toBe(120);
    });

    it('should throw for negative numbers', () => {
      expect(() => mathOps.factorial(-1)).toThrow('Factorial is not defined for negative numbers');
    });
  });

  describe('pi', () => {
    it('should return the first 40 decimals of pi', () => {
      expect(mathOps.pi()).toBe('3.1415926535897932384626433832795028841971');
    });
  });

  describe('gcd', () => {
    it('should correctly calculate greatest common divisor', () => {
      expect(mathOps.gcd(1, 1)).toBe(1);
      expect(mathOps.gcd(10, 15)).toBe(5);
      expect(mathOps.gcd(48, 18)).toBe(6);
      expect(mathOps.gcd(17, 19)).toBe(1);
    });

    it('should handle negative numbers', () => {
      expect(mathOps.gcd(-10, 15)).toBe(5);
      expect(mathOps.gcd(48, -18)).toBe(6);
      expect(mathOps.gcd(-14, -21)).toBe(7);
    });
  });

  describe('derivative', () => {
    it('should return correct derivative coefficients', () => {
      expect(mathOps.derivative([3, 2, 5])).toEqual([2, 10]);
      expect(mathOps.derivative([0, 0, 0, 1])).toEqual([0, 0, 3]);
      expect(mathOps.derivative([7])).toEqual([0]);
    });

    it('should return zero for empty polynomial', () => {
      expect(mathOps.derivative([])).toEqual([0]);
    });

    it('should throw for null coefficients', () => {
      expect(() => mathOps.derivative(null as unknown as number[])).toThrow('Coefficients array must not be null');
    });
  });
});
