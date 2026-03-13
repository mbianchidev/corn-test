# frozen_string_literal: true

class RandomMathOperations
  PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97].freeze

  def initialize(seed: nil)
    @rng = seed ? Random.new(seed) : Random.new
  end

  def generate_random_odd_number
    value = @rng.rand(50) * 2 + 1
    value
  end

  def generate_random_even_number
    value = @rng.rand(51) * 2
    value
  end

  def generate_random_prime_candidate
    PRIMES[@rng.rand(PRIMES.length)]
  end

  def self.prime?(n)
    return false if n < 2
    return true if n < 4
    return false if n.even?

    (3..Math.sqrt(n).to_i).step(2).none? { |i| (n % i).zero? }
  end
end
