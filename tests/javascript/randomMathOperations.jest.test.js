const { RandomMathOperations } = require('./randomMathOperations');

describe('RandomMathOperations (Jest) - Intentionally Flaky', () => {
  let randomOps;

  beforeEach(() => {
    randomOps = new RandomMathOperations();
  });

  // Run 20 times to detect flakiness
  describe.each(Array.from({ length: 20 }, (_, i) => [i + 1]))('Run %i/20', (run) => {
    test('random odd number should be odd', () => {
      const number = randomOps.generateRandomOddNumber();
      expect(number).toBeGreaterThanOrEqual(1);
      expect(number).toBeLessThanOrEqual(100);
      expect(number % 2).toBe(1);
    });

    test('random even number should be even', () => {
      const number = randomOps.generateRandomEvenNumber();
      expect(number).toBeGreaterThanOrEqual(0);
      expect(number).toBeLessThanOrEqual(100);
      expect(number % 2).toBe(0);
    });

    test('random prime candidate should be prime', () => {
      const number = randomOps.generateRandomPrimeCandidate();
      expect(number).toBeGreaterThanOrEqual(2);
      expect(number).toBeLessThanOrEqual(200);
      expect(RandomMathOperations.isPrime(number)).toBe(true);
    });
  });

  describe('isPrime helper', () => {
    test('should correctly identify prime numbers', () => {
      expect(RandomMathOperations.isPrime(2)).toBe(true);
      expect(RandomMathOperations.isPrime(3)).toBe(true);
      expect(RandomMathOperations.isPrime(5)).toBe(true);
      expect(RandomMathOperations.isPrime(7)).toBe(true);
      expect(RandomMathOperations.isPrime(11)).toBe(true);
      expect(RandomMathOperations.isPrime(97)).toBe(true);
    });

    test('should correctly identify non-prime numbers', () => {
      expect(RandomMathOperations.isPrime(1)).toBe(false);
      expect(RandomMathOperations.isPrime(4)).toBe(false);
      expect(RandomMathOperations.isPrime(6)).toBe(false);
      expect(RandomMathOperations.isPrime(9)).toBe(false);
      expect(RandomMathOperations.isPrime(100)).toBe(false);
    });
  });
});
