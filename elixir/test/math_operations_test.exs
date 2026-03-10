defmodule CornTest.MathOperationsTest do
  use ExUnit.Case, async: true

  alias CornTest.MathOperations

  describe "add/2" do
    test "adds two positive numbers" do
      assert MathOperations.add(2, 3) == 5
      assert MathOperations.add(40, 60) == 100
    end

    test "adds negative numbers" do
      assert MathOperations.add(-2, -3) == -5
      assert MathOperations.add(5, -5) == 0
    end
  end

  describe "subtract/2" do
    test "subtracts two numbers" do
      assert MathOperations.subtract(5, 3) == 2
      assert MathOperations.subtract(3, 5) == -2
      assert MathOperations.subtract(10, 10) == 0
    end
  end

  describe "multiply/2" do
    test "multiplies two numbers" do
      assert MathOperations.multiply(2, 3) == 6
      assert MathOperations.multiply(-2, 3) == -6
      assert MathOperations.multiply(0, 100) == 0
    end
  end

  describe "divide/2" do
    test "divides two numbers" do
      assert MathOperations.divide(6, 3) == {:ok, 2.0}
      assert MathOperations.divide(5, 2) == {:ok, 2.5}
    end

    test "returns error for division by zero" do
      assert MathOperations.divide(5, 0) == {:error, "Division by zero"}
    end
  end

  describe "power/2" do
    test "calculates power" do
      assert MathOperations.power(2, 3) == 8.0
      assert MathOperations.power(5, 0) == 1.0
    end
  end

  describe "factorial/1" do
    test "calculates factorial" do
      assert MathOperations.factorial(0) == {:ok, 1}
      assert MathOperations.factorial(1) == {:ok, 1}
      assert MathOperations.factorial(5) == {:ok, 120}
    end

    test "returns error for negative numbers" do
      assert MathOperations.factorial(-1) == {:error, "Factorial is not defined for negative numbers"}
    end
  end

  describe "derivative/1" do
    test "calculates derivative of polynomial" do
      assert MathOperations.derivative([3, 2, 5]) == [2, 10]
      assert MathOperations.derivative([7]) == [0.0]
      assert MathOperations.derivative([]) == [0.0]
    end
  end

  describe "pi/0" do
    test "returns first 40 decimals of pi" do
      assert MathOperations.pi() == "3.1415926535897932384626433832795028841971"
    end
  end

  describe "gcd/2" do
    test "calculates greatest common divisor" do
      assert MathOperations.gcd(10, 15) == 5
      assert MathOperations.gcd(48, 18) == 6
      assert MathOperations.gcd(17, 19) == 1
    end

    test "handles negative numbers" do
      assert MathOperations.gcd(-10, 15) == 5
      assert MathOperations.gcd(48, -18) == 6
    end
  end
end
