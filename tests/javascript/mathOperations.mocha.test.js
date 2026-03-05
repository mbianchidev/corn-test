const { expect } = require('chai');
const { MathOperations } = require('./mathOperations');

describe('MathOperations (Mocha)', function () {
  let mathOps;

  beforeEach(function () {
    mathOps = new MathOperations();
  });

  describe('add', function () {
    it('should correctly add two positive numbers', function () {
      expect(mathOps.add(2, 3)).to.equal(5);
      expect(mathOps.add(40, 60)).to.equal(100);
    });

    it('should correctly handle negative numbers', function () {
      expect(mathOps.add(-2, -3)).to.equal(-5);
      expect(mathOps.add(5, -5)).to.equal(0);
    });
  });

  describe('subtract', function () {
    it('should correctly subtract two numbers', function () {
      expect(mathOps.subtract(5, 3)).to.equal(2);
      expect(mathOps.subtract(3, 5)).to.equal(-2);
      expect(mathOps.subtract(10, 10)).to.equal(0);
    });
  });

  describe('multiply', function () {
    it('should correctly multiply two numbers', function () {
      expect(mathOps.multiply(2, 3)).to.equal(6);
      expect(mathOps.multiply(-2, 3)).to.equal(-6);
      expect(mathOps.multiply(0, 100)).to.equal(0);
    });
  });

  describe('divide', function () {
    it('should correctly divide two numbers', function () {
      expect(mathOps.divide(6, 3)).to.be.closeTo(2.0, 0.001);
      expect(mathOps.divide(5, 2)).to.be.closeTo(2.5, 0.001);
      expect(mathOps.divide(6, -3)).to.be.closeTo(-2.0, 0.001);
    });

    it('should throw on division by zero', function () {
      expect(() => mathOps.divide(5, 0)).to.throw('Division by zero');
    });
  });

  describe('power', function () {
    it('should correctly calculate exponentials', function () {
      expect(mathOps.power(2, 3)).to.be.closeTo(8.0, 0.001);
      expect(mathOps.power(5, 0)).to.be.closeTo(1.0, 0.001);
      expect(mathOps.power(2, -2)).to.be.closeTo(0.25, 0.001);
    });
  });

  describe('factorial', function () {
    it('should correctly calculate factorials', function () {
      expect(mathOps.factorial(0)).to.equal(1);
      expect(mathOps.factorial(1)).to.equal(1);
      expect(mathOps.factorial(2)).to.equal(2);
      expect(mathOps.factorial(3)).to.equal(6);
      expect(mathOps.factorial(4)).to.equal(24);
      expect(mathOps.factorial(5)).to.equal(120);
    });

    it('should throw for negative numbers', function () {
      expect(() => mathOps.factorial(-1)).to.throw('Factorial is not defined for negative numbers');
    });
  });

  describe('pi', function () {
    it('should return the first 40 decimals of pi', function () {
      expect(mathOps.pi()).to.equal('3.1415926535897932384626433832795028841971');
    });
  });

  describe('gcd', function () {
    it('should correctly calculate greatest common divisor', function () {
      expect(mathOps.gcd(1, 1)).to.equal(1);
      expect(mathOps.gcd(10, 15)).to.equal(5);
      expect(mathOps.gcd(48, 18)).to.equal(6);
      expect(mathOps.gcd(17, 19)).to.equal(1);
    });

    it('should handle negative numbers', function () {
      expect(mathOps.gcd(-10, 15)).to.equal(5);
      expect(mathOps.gcd(48, -18)).to.equal(6);
      expect(mathOps.gcd(-14, -21)).to.equal(7);
    });
  });

  describe('derivative', function () {
    it('should return correct derivative coefficients', function () {
      expect(mathOps.derivative([3, 2, 5])).to.deep.equal([2, 10]);
      expect(mathOps.derivative([0, 0, 0, 1])).to.deep.equal([0, 0, 3]);
      expect(mathOps.derivative([7])).to.deep.equal([0]);
    });

    it('should return zero for empty polynomial', function () {
      expect(mathOps.derivative([])).to.deep.equal([0]);
    });

    it('should throw for null coefficients', function () {
      expect(() => mathOps.derivative(null)).to.throw('Coefficients array must not be null');
    });
  });
});
