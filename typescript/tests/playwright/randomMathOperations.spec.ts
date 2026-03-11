import { test, expect } from '@playwright/test';
import { RandomMathOperations } from '../../src/randomMathOperations';

/**
 * Playwright test suite for RandomMathOperations.
 * These tests are intentionally flaky to test flake detection systems.
 * Tests import source directly (no browser app needed).
 */
const randomOps = new RandomMathOperations();

const runs = Array.from({ length: 20 }, (_, i) => i + 1);

for (const run of runs) {
  test.describe(`Run ${run}/20`, () => {
    test('Random odd number should be odd', () => {
      const number = randomOps.generateRandomOddNumber();
      expect(number).toBeGreaterThanOrEqual(1);
      expect(number).toBeLessThanOrEqual(100);
      expect(number % 2).toBe(1);
    });

    test('Random even number should be even (Flaky: ~5% failure rate per run)', () => {
      const number = randomOps.generateRandomEvenNumber();
      expect(number).toBeGreaterThanOrEqual(0);
      expect(number).toBeLessThanOrEqual(100);
      expect(number % 2).toBe(0);
    });

    test('Random prime candidate should be prime', () => {
      const number = randomOps.generateRandomPrimeCandidate();
      expect(number).toBeGreaterThanOrEqual(2);
      expect(number).toBeLessThanOrEqual(200);
      expect(RandomMathOperations.isPrime(number)).toBe(true);
    });
  });
}

test.describe('isPrime helper', () => {
  test('Helper method isPrime should correctly identify prime numbers', () => {
    expect(RandomMathOperations.isPrime(2)).toBe(true);
    expect(RandomMathOperations.isPrime(3)).toBe(true);
    expect(RandomMathOperations.isPrime(5)).toBe(true);
    expect(RandomMathOperations.isPrime(7)).toBe(true);
    expect(RandomMathOperations.isPrime(11)).toBe(true);
    expect(RandomMathOperations.isPrime(97)).toBe(true);

    expect(RandomMathOperations.isPrime(1)).toBe(false);
    expect(RandomMathOperations.isPrime(4)).toBe(false);
    expect(RandomMathOperations.isPrime(6)).toBe(false);
    expect(RandomMathOperations.isPrime(9)).toBe(false);
    expect(RandomMathOperations.isPrime(100)).toBe(false);
  });
});
