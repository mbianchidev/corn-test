defmodule CornTest.MathOperations do
  @moduledoc """
  Deterministic mathematical operations.
  """

  @spec add(number(), number()) :: number()
  def add(a, b), do: a + b

  @spec subtract(number(), number()) :: number()
  def subtract(a, b), do: a - b

  @spec multiply(number(), number()) :: number()
  def multiply(a, b), do: a * b

  @spec divide(number(), number()) :: {:ok, float()} | {:error, String.t()}
  def divide(_a, 0), do: {:error, "Division by zero"}
  def divide(a, b), do: {:ok, a / b}

  @spec power(number(), integer()) :: float()
  def power(base, exponent), do: :math.pow(base, exponent)

  @spec factorial(integer()) :: {:ok, integer()} | {:error, String.t()}
  def factorial(n) when n < 0, do: {:error, "Factorial is not defined for negative numbers"}
  def factorial(0), do: {:ok, 1}
  def factorial(1), do: {:ok, 1}
  def factorial(n), do: {:ok, Enum.reduce(2..n, 1, &(&1 * &2))}

  @spec derivative([float()]) :: [float()]
  def derivative([]), do: [0.0]
  def derivative([_]), do: [0.0]

  def derivative(coefficients) do
    coefficients
    |> Enum.with_index()
    |> Enum.drop(1)
    |> Enum.map(fn {coeff, idx} -> coeff * idx end)
  end

  @spec pi() :: String.t()
  def pi, do: "3.1415926535897932384626433832795028841971"

  @spec gcd(integer(), integer()) :: integer()
  def gcd(a, b) do
    a = abs(a)
    b = abs(b)
    do_gcd(a, b)
  end

  defp do_gcd(a, 0), do: a
  defp do_gcd(a, b), do: do_gcd(b, rem(a, b))
end
