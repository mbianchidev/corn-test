// Package mathops contains mathematical operations for testing.
package mathops

import (
	"errors"
	"math"
)

// MathOperations contains deterministic mathematical operations.
type MathOperations struct{}

// Add adds two integers.
func (m *MathOperations) Add(a, b int) int {
	return a + b
}

// Subtract subtracts two integers.
func (m *MathOperations) Subtract(a, b int) int {
	return a - b
}

// Multiply multiplies two integers.
func (m *MathOperations) Multiply(a, b int) int {
	return a * b
}

// Divide divides two numbers. Returns error if divisor is zero.
func (m *MathOperations) Divide(a, b int) (float64, error) {
	if b == 0 {
		return 0, errors.New("division by zero")
	}
	return float64(a) / float64(b), nil
}

// Power calculates the power of a number.
func (m *MathOperations) Power(base float64, exponent int) float64 {
	return math.Pow(base, float64(exponent))
}

// Factorial calculates the factorial of a number. Returns error if n is negative.
func (m *MathOperations) Factorial(n int) (int64, error) {
	if n < 0 {
		return 0, errors.New("factorial is not defined for negative numbers")
	}
	if n == 0 || n == 1 {
		return 1, nil
	}
	var result int64 = 1
	for i := 2; i <= n; i++ {
		result *= int64(i)
	}
	return result, nil
}

// Derivative computes the derivative of a polynomial represented by its coefficients.
// coefficients[0] + coefficients[1]*x + coefficients[2]*x^2 + ...
func (m *MathOperations) Derivative(coefficients []float64) ([]float64, error) {
	if coefficients == nil {
		return nil, errors.New("coefficients slice must not be nil")
	}
	if len(coefficients) <= 1 {
		return []float64{0}, nil
	}
	result := make([]float64, len(coefficients)-1)
	for i := 1; i < len(coefficients); i++ {
		result[i-1] = coefficients[i] * float64(i)
	}
	return result, nil
}

// Pi returns the first 40 decimals of the pi constant.
func (m *MathOperations) Pi() string {
	return "3.1415926535897932384626433832795028841971"
}

// GCD calculates the greatest common divisor using Euclidean algorithm.
func (m *MathOperations) GCD(a, b int) int {
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
