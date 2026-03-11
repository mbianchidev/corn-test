package mathops

import (
	"math"
	"testing"
)

func TestAdd(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		{"positive numbers", 2, 3, 5},
		{"negative numbers", -2, -3, -5},
		{"mixed signs", -2, 3, 1},
		{"zeros", 0, 0, 0},
		{"large numbers", 1000000, 2000000, 3000000},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Add(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
			}
		})
	}
}

func TestSubtract(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		{"positive numbers", 5, 3, 2},
		{"negative result", 3, 5, -2},
		{"negative numbers", -2, -3, 1},
		{"zeros", 0, 0, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Subtract(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("Subtract(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
			}
		})
	}
}

func TestMultiply(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		{"positive numbers", 4, 5, 20},
		{"negative numbers", -3, -4, 12},
		{"mixed signs", -3, 4, -12},
		{"by zero", 5, 0, 0},
		{"by one", 7, 1, 7},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Multiply(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("Multiply(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
			}
		})
	}
}

func TestDivide(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected float64
		wantErr  bool
	}{
		{"exact division", 10, 2, 5.0, false},
		{"fractional result", 7, 2, 3.5, false},
		{"negative division", -10, 2, -5.0, false},
		{"division by zero", 10, 0, 0, true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Divide(tt.a, tt.b)
			if tt.wantErr {
				if err == nil {
					t.Errorf("Divide(%d, %d) expected error, got nil", tt.a, tt.b)
				}
			} else {
				if err != nil {
					t.Errorf("Divide(%d, %d) unexpected error: %v", tt.a, tt.b, err)
				}
				if math.Abs(result-tt.expected) > 1e-9 {
					t.Errorf("Divide(%d, %d) = %f, want %f", tt.a, tt.b, result, tt.expected)
				}
			}
		})
	}
}

func TestPower(t *testing.T) {
	tests := []struct {
		name     string
		base     float64
		exp      int
		expected float64
	}{
		{"square", 2.0, 2, 4.0},
		{"cube", 3.0, 3, 27.0},
		{"power of zero", 5.0, 0, 1.0},
		{"power of one", 7.0, 1, 7.0},
		{"negative exponent", 2.0, -1, 0.5},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Power(tt.base, tt.exp)
			if math.Abs(result-tt.expected) > 1e-9 {
				t.Errorf("Power(%f, %d) = %f, want %f", tt.base, tt.exp, result, tt.expected)
			}
		})
	}
}

func TestFactorial(t *testing.T) {
	tests := []struct {
		name     string
		n        int
		expected int64
	}{
		{"zero", 0, 1},
		{"one", 1, 1},
		{"five", 5, 120},
		{"ten", 10, 3628800},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Factorial(tt.n)
			if result != tt.expected {
				t.Errorf("Factorial(%d) = %d, want %d", tt.n, result, tt.expected)
			}
		})
	}
}

func TestFactorialNegativePanics(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Factorial(-1) should panic")
		}
	}()
	Factorial(-1)
}

func TestDerivative(t *testing.T) {
	tests := []struct {
		name     string
		coeffs   []float64
		expected []float64
	}{
		{"constant", []float64{5}, []float64{0}},
		{"linear", []float64{3, 2}, []float64{2}},
		{"quadratic", []float64{3, 2, 1}, []float64{2, 2}},
		{"cubic", []float64{1, 0, 3, 4}, []float64{0, 6, 12}},
		{"empty", []float64{}, []float64{0}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Derivative(tt.coeffs)
			if len(result) != len(tt.expected) {
				t.Fatalf("Derivative(%v) returned %d elements, want %d", tt.coeffs, len(result), len(tt.expected))
			}
			for i := range result {
				if math.Abs(result[i]-tt.expected[i]) > 1e-9 {
					t.Errorf("Derivative(%v)[%d] = %f, want %f", tt.coeffs, i, result[i], tt.expected[i])
				}
			}
		})
	}
}

func TestPi(t *testing.T) {
	expected := "3.1415926535897932384626433832795028841971"
	result := Pi()
	if result != expected {
		t.Errorf("Pi() = %q, want %q", result, expected)
	}
}

func TestGCD(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		{"common case", 12, 8, 4},
		{"coprime", 7, 13, 1},
		{"same numbers", 5, 5, 5},
		{"one is zero", 10, 0, 10},
		{"both zero", 0, 0, 0},
		{"negative numbers", -12, 8, 4},
		{"large numbers", 48, 18, 6},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GCD(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("GCD(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
			}
		})
	}
}
