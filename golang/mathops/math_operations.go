package mathops

import (
	"errors"
	"math"
)

// Add returns the sum of two integers.
func Add(a, b int) int {
	return a + b
}

// Subtract returns the difference of two integers.
func Subtract(a, b int) int {
	return a - b
}

// Multiply returns the product of two integers.
func Multiply(a, b int) int {
	return a * b
}

// Divide returns the quotient of two integers as a float64.
// Returns an error if b is zero.
func Divide(a, b int) (float64, error) {
	if b == 0 {
		return 0, errors.New("division by zero")
	}
	return float64(a) / float64(b), nil
}

// Power returns base raised to the given exponent.
func Power(base float64, exponent int) float64 {
	return math.Pow(base, float64(exponent))
}

// Factorial returns the factorial of n.
// Panics if n is negative.
func Factorial(n int) int64 {
	if n < 0 {
		panic("factorial is not defined for negative numbers")
	}
	if n == 0 || n == 1 {
		return 1
	}
	var result int64 = 1
	for i := 2; i <= n; i++ {
		result *= int64(i)
	}
	return result
}

// Derivative computes the derivative of a polynomial represented by its
// coefficients. The index of each coefficient corresponds to the power of x.
// For example, [3, 2, 1] represents 3 + 2x + x² and its derivative is [2, 2].
func Derivative(coefficients []float64) []float64 {
	if len(coefficients) <= 1 {
		return []float64{0}
	}
	result := make([]float64, len(coefficients)-1)
	for i := 1; i < len(coefficients); i++ {
		result[i-1] = float64(i) * coefficients[i]
	}
	return result
}

// Pi returns a string representation of pi to 40 decimal places.
func Pi() string {
	return "3.1415926535897932384626433832795028841971"
}

// GCD returns the greatest common divisor of two integers using
// the Euclidean algorithm.
func GCD(a, b int) int {
	if a < 0 {
		a = -a
	}
	if b < 0 {
		b = -b
	}
	for b != 0 {
		a, b = b, a%b
	}
	return a
}
