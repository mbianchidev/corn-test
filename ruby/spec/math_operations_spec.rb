# frozen_string_literal: true

require_relative '../lib/math_operations'

RSpec.describe MathOperations do
  subject(:math) { described_class.new }

  describe '#add' do
    it 'adds two positive numbers' do
      expect(math.add(2, 3)).to eq(5)
    end

    it 'adds negative numbers' do
      expect(math.add(-1, -2)).to eq(-3)
    end

    it 'adds zero' do
      expect(math.add(5, 0)).to eq(5)
    end
  end

  describe '#subtract' do
    it 'subtracts two positive numbers' do
      expect(math.subtract(5, 3)).to eq(2)
    end

    it 'subtracts resulting in negative' do
      expect(math.subtract(3, 5)).to eq(-2)
    end

    it 'subtracts zero' do
      expect(math.subtract(5, 0)).to eq(5)
    end
  end

  describe '#multiply' do
    it 'multiplies two positive numbers' do
      expect(math.multiply(3, 4)).to eq(12)
    end

    it 'multiplies by zero' do
      expect(math.multiply(5, 0)).to eq(0)
    end

    it 'multiplies negative numbers' do
      expect(math.multiply(-3, -4)).to eq(12)
    end
  end

  describe '#divide' do
    it 'divides two numbers' do
      expect(math.divide(10, 2)).to eq(5.0)
    end

    it 'divides with decimal result' do
      expect(math.divide(7, 2)).to eq(3.5)
    end

    context 'when dividing by zero' do
      it 'raises ZeroDivisionError' do
        expect { math.divide(10, 0) }.to raise_error(ZeroDivisionError)
      end
    end
  end

  describe '#power' do
    it 'calculates positive exponent' do
      expect(math.power(2, 3)).to eq(8)
    end

    it 'calculates zero exponent' do
      expect(math.power(5, 0)).to eq(1)
    end

    it 'calculates negative exponent' do
      expect(math.power(2, -1)).to eq(0.5)
    end
  end

  describe '#factorial' do
    it 'calculates factorial of positive number' do
      expect(math.factorial(5)).to eq(120)
    end

    it 'calculates factorial of zero' do
      expect(math.factorial(0)).to eq(1)
    end

    it 'calculates factorial of one' do
      expect(math.factorial(1)).to eq(1)
    end

    context 'when n is negative' do
      it 'raises ArgumentError' do
        expect { math.factorial(-1) }.to raise_error(ArgumentError)
      end
    end
  end

  describe '#derivative' do
    it 'calculates derivative of polynomial' do
      expect(math.derivative([3, 2, 1])).to eq([2, 2])
    end

    it 'calculates derivative of linear function' do
      expect(math.derivative([5, 3])).to eq([3])
    end

    it 'returns empty array for constant' do
      expect(math.derivative([5])).to eq([])
    end

    it 'returns empty array for empty input' do
      expect(math.derivative([])).to eq([])
    end

    context 'when coefficients are nil' do
      it 'raises ArgumentError' do
        expect { math.derivative(nil) }.to raise_error(ArgumentError)
      end
    end
  end

  describe '#pi' do
    it 'returns pi as a string' do
      expect(math.pi).to start_with('3.14159265358979')
    end

    it 'returns consistent value' do
      expect(math.pi).to eq(math.pi)
    end
  end

  describe '#gcd' do
    it 'calculates gcd of two positive numbers' do
      expect(math.gcd(12, 8)).to eq(4)
    end

    it 'calculates gcd when one number is zero' do
      expect(math.gcd(5, 0)).to eq(5)
    end

    it 'calculates gcd of negative numbers' do
      expect(math.gcd(-12, 8)).to eq(4)
    end

    it 'calculates gcd of coprime numbers' do
      expect(math.gcd(7, 13)).to eq(1)
    end
  end
end
