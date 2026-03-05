const { expect } = require('chai');
const { RandomMathOperations } = require('./randomMathOperations');

describe('RandomMathOperations (Mocha) - Intentionally Flaky', function () {
  let randomOps;

  beforeEach(function () {
    randomOps = new RandomMathOperations();
  });

  // Run 20 times to detect flakiness
  for (let run = 1; run <= 20; run++) {
    describe(`Run ${run}/20`, function () {
      it('random odd number should be odd', function () {
        const number = randomOps.generateRandomOddNumber();
        expect(number).to.be.at.least(1);
        expect(number).to.be.at.most(100);
        expect(number % 2).to.equal(1);
      });

      it('random even number should be even', function () {
        const number = randomOps.generateRandomEvenNumber();
        expect(number).to.be.at.least(0);
        expect(number).to.be.at.most(100);
        expect(number % 2).to.equal(0);
      });

      it('random prime candidate should be prime', function () {
        const number = randomOps.generateRandomPrimeCandidate();
        expect(number).to.be.at.least(2);
        expect(number).to.be.at.most(200);
        expect(RandomMathOperations.isPrime(number)).to.equal(true);
      });
    });
  }

  describe('isPrime helper', function () {
    it('should correctly identify prime numbers', function () {
      expect(RandomMathOperations.isPrime(2)).to.equal(true);
      expect(RandomMathOperations.isPrime(3)).to.equal(true);
      expect(RandomMathOperations.isPrime(5)).to.equal(true);
      expect(RandomMathOperations.isPrime(7)).to.equal(true);
      expect(RandomMathOperations.isPrime(11)).to.equal(true);
      expect(RandomMathOperations.isPrime(97)).to.equal(true);
    });

    it('should correctly identify non-prime numbers', function () {
      expect(RandomMathOperations.isPrime(1)).to.equal(false);
      expect(RandomMathOperations.isPrime(4)).to.equal(false);
      expect(RandomMathOperations.isPrime(6)).to.equal(false);
      expect(RandomMathOperations.isPrime(9)).to.equal(false);
      expect(RandomMathOperations.isPrime(100)).to.equal(false);
    });
  });
});
