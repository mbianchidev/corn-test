# frozen_string_literal: true

class MathOperations
  def add(a, b)
    a + b
  end

  def subtract(a, b)
    a - b
  end

  def multiply(a, b)
    a * b
  end

  def divide(a, b)
    raise ZeroDivisionError, 'Cannot divide by zero' if b.zero?

    a.to_f / b
  end

  def power(base, exponent)
    base**exponent
  end

  def factorial(n)
    raise ArgumentError, 'Factorial is not defined for negative numbers' if n.negative?

    return 1 if n.zero?

    (1..n).reduce(:*)
  end

  def derivative(coefficients)
    raise ArgumentError, 'Coefficients cannot be nil' if coefficients.nil?
    return [] if coefficients.length <= 1

    coefficients.each_with_index.filter_map do |coeff, i|
      next if i.zero?

      coeff * i
    end
  end

  def pi
    '3.1415926535897932384626433832795028841971'
  end

  def gcd(a, b)
    a = a.abs
    b = b.abs
    b.zero? ? a : gcd(b, a % b)
  end
end
