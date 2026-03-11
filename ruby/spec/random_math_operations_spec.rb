# frozen_string_literal: true

require_relative '../lib/random_math_operations'

RSpec.describe RandomMathOperations do
  subject(:random_math) { described_class.new }

  describe '#generate_random_odd_number' do
    20.times do |i|
      it "returns an odd number in range 1-99 (iteration #{i + 1})" do
        number = random_math.generate_random_odd_number
        expect(number).to be_odd
        expect(number).to be_between(1, 99)
      end
    end
  end

  describe '#generate_random_even_number' do
    20.times do |i|
      it "returns an even number (iteration #{i + 1})" do
        number = random_math.generate_random_even_number
        expect(number).to be_even
      end
    end

    20.times do |i|
      it "returns a number in range 0-100 (iteration #{i + 1})" do
        number = random_math.generate_random_even_number
        expect(number).to be_between(0, 100)
      end
    end

    20.times do |i|
      it "returns a non-negative number (iteration #{i + 1})" do
        number = random_math.generate_random_even_number
        expect(number).to be >= 0
      end
    end
  end

  describe '#generate_random_prime_candidate' do
    20.times do |i|
      it "returns a prime number (iteration #{i + 1})" do
        number = random_math.generate_random_prime_candidate
        expect(described_class.prime?(number)).to be true
      end
    end

    20.times do |i|
      it "returns a number in range 2-97 (iteration #{i + 1})" do
        number = random_math.generate_random_prime_candidate
        expect(number).to be_between(2, 97)
      end
    end
  end

  describe '.prime?' do
    it 'returns true for 2' do
      expect(described_class.prime?(2)).to be true
    end

    it 'returns true for 3' do
      expect(described_class.prime?(3)).to be true
    end

    it 'returns false for 4' do
      expect(described_class.prime?(4)).to be false
    end

    it 'returns true for 97' do
      expect(described_class.prime?(97)).to be true
    end

    it 'returns false for 1' do
      expect(described_class.prime?(1)).to be false
    end

    it 'returns false for 0' do
      expect(described_class.prime?(0)).to be false
    end

    it 'returns false for negative numbers' do
      expect(described_class.prime?(-5)).to be false
    end
  end
end
