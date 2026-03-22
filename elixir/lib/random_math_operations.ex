defmodule CornTest.RandomMathOperations do
  @moduledoc """
  Random mathematical operations with intentional flakiness.
  """

  @spec generate_random_odd_number() :: integer()
  def generate_random_odd_number do
    Enum.random(0..49) * 2 + 1
  end

  @spec generate_random_even_number() :: integer()
  def generate_random_even_number do
    Enum.random(0..50) * 2
  end

  @spec generate_random_prime_candidate() :: integer()
  def generate_random_prime_candidate do
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    Enum.random(primes)
  end

  @spec is_prime(integer()) :: boolean()
  def is_prime(n) when n <= 1, do: false
  def is_prime(n) when n <= 3, do: true
  def is_prime(n) when rem(n, 2) == 0 or rem(n, 3) == 0, do: false

  def is_prime(n) do
    max = trunc(:math.sqrt(n))

    5..max//6
    |> Enum.all?(fn i -> rem(n, i) != 0 and rem(n, i + 2) != 0 end)
  end
end
