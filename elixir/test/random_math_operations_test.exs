defmodule CornTest.RandomMathOperationsTest do
  use ExUnit.Case, async: true

  alias CornTest.RandomMathOperations

  describe "generate_random_odd_number/0" do
    test "generates odd numbers between 1 and 99 (20 iterations)" do
      Enum.each(1..20, fn _ ->
        number = RandomMathOperations.generate_random_odd_number()
        assert number >= 1 and number <= 99, "Number should be between 1 and 99, got: #{number}"
        assert rem(number, 2) == 1, "Number should be odd, got: #{number}"
      end)
    end
  end

  describe "generate_random_even_number/0" do
    test "generates even numbers between 0 and 100 (20 iterations)" do
      Enum.each(1..20, fn _ ->
        number = RandomMathOperations.generate_random_even_number()
        assert number >= 0 and number <= 100, "Number should be between 0 and 100, got: #{number}"
        assert rem(number, 2) == 0, "Number should be even, got: #{number}"
      end)
    end
  end

  describe "generate_random_prime_candidate/0" do
    test "generates prime numbers between 2 and 97 (20 iterations)" do
      Enum.each(1..20, fn _ ->
        number = RandomMathOperations.generate_random_prime_candidate()
        assert number >= 2 and number <= 97, "Number should be between 2 and 97, got: #{number}"
        assert RandomMathOperations.is_prime(number), "Number should be prime, got: #{number}"
      end)
    end
  end

  describe "is_prime/1" do
    test "correctly identifies prime numbers" do
      assert RandomMathOperations.is_prime(2)
      assert RandomMathOperations.is_prime(3)
      assert RandomMathOperations.is_prime(5)
      assert RandomMathOperations.is_prime(97)
    end

    test "correctly identifies non-prime numbers" do
      refute RandomMathOperations.is_prime(1)
      refute RandomMathOperations.is_prime(4)
      refute RandomMathOperations.is_prime(100)
    end
  end
end
