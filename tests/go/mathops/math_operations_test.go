package mathops

import (
	"math"
	"testing"
)

func TestAdd(t *testing.T) {
	m := &MathOperations{}

	t.Run("positive numbers", func(t *testing.T) {
		if got := m.Add(2, 3); got != 5 {
			t.Errorf("Add(2, 3) = %d, want 5", got)
		}
		if got := m.Add(40, 60); got != 100 {
			t.Errorf("Add(40, 60) = %d, want 100", got)
		}
	})

	t.Run("negative numbers", func(t *testing.T) {
		if got := m.Add(-2, -3); got != -5 {
			t.Errorf("Add(-2, -3) = %d, want -5", got)
		}
		if got := m.Add(5, -5); got != 0 {
			t.Errorf("Add(5, -5) = %d, want 0", got)
		}
	})
}

func TestSubtract(t *testing.T) {
	m := &MathOperations{}

	if got := m.Subtract(5, 3); got != 2 {
		t.Errorf("Subtract(5, 3) = %d, want 2", got)
	}
	if got := m.Subtract(3, 5); got != -2 {
		t.Errorf("Subtract(3, 5) = %d, want -2", got)
	}
	if got := m.Subtract(10, 10); got != 0 {
		t.Errorf("Subtract(10, 10) = %d, want 0", got)
	}
}

func TestMultiply(t *testing.T) {
	m := &MathOperations{}

	if got := m.Multiply(2, 3); got != 6 {
		t.Errorf("Multiply(2, 3) = %d, want 6", got)
	}
	if got := m.Multiply(-2, 3); got != -6 {
		t.Errorf("Multiply(-2, 3) = %d, want -6", got)
	}
	if got := m.Multiply(0, 100); got != 0 {
		t.Errorf("Multiply(0, 100) = %d, want 0", got)
	}
}

func TestDivide(t *testing.T) {
	m := &MathOperations{}

	t.Run("valid division", func(t *testing.T) {
		got, err := m.Divide(6, 3)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if math.Abs(got-2.0) > 0.001 {
			t.Errorf("Divide(6, 3) = %f, want 2.0", got)
		}

		got, err = m.Divide(5, 2)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if math.Abs(got-2.5) > 0.001 {
			t.Errorf("Divide(5, 2) = %f, want 2.5", got)
		}

		got, err = m.Divide(6, -3)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if math.Abs(got-(-2.0)) > 0.001 {
			t.Errorf("Divide(6, -3) = %f, want -2.0", got)
		}
	})

	t.Run("division by zero", func(t *testing.T) {
		_, err := m.Divide(5, 0)
		if err == nil {
			t.Error("expected error for division by zero")
		}
	})
}

func TestPower(t *testing.T) {
	m := &MathOperations{}

	if got := m.Power(2, 3); math.Abs(got-8.0) > 0.001 {
		t.Errorf("Power(2, 3) = %f, want 8.0", got)
	}
	if got := m.Power(5, 0); math.Abs(got-1.0) > 0.001 {
		t.Errorf("Power(5, 0) = %f, want 1.0", got)
	}
	if got := m.Power(2, -2); math.Abs(got-0.25) > 0.001 {
		t.Errorf("Power(2, -2) = %f, want 0.25", got)
	}
}

func TestFactorial(t *testing.T) {
	m := &MathOperations{}

	t.Run("valid factorials", func(t *testing.T) {
		cases := []struct {
			n    int
			want int64
		}{
			{0, 1}, {1, 1}, {2, 2}, {3, 6}, {4, 24}, {5, 120},
		}
		for _, tc := range cases {
			got, err := m.Factorial(tc.n)
			if err != nil {
				t.Fatalf("Factorial(%d): unexpected error: %v", tc.n, err)
			}
			if got != tc.want {
				t.Errorf("Factorial(%d) = %d, want %d", tc.n, got, tc.want)
			}
		}
	})

	t.Run("negative number", func(t *testing.T) {
		_, err := m.Factorial(-1)
		if err == nil {
			t.Error("expected error for negative factorial")
		}
	})
}

func TestPi(t *testing.T) {
	m := &MathOperations{}
	expected := "3.1415926535897932384626433832795028841971"
	if got := m.Pi(); got != expected {
		t.Errorf("Pi() = %s, want %s", got, expected)
	}
}

func TestGCD(t *testing.T) {
	m := &MathOperations{}

	t.Run("positive numbers", func(t *testing.T) {
		cases := []struct {
			a, b, want int
		}{
			{1, 1, 1}, {10, 15, 5}, {48, 18, 6}, {17, 19, 1},
		}
		for _, tc := range cases {
			if got := m.GCD(tc.a, tc.b); got != tc.want {
				t.Errorf("GCD(%d, %d) = %d, want %d", tc.a, tc.b, got, tc.want)
			}
		}
	})

	t.Run("negative numbers", func(t *testing.T) {
		cases := []struct {
			a, b, want int
		}{
			{-10, 15, 5}, {48, -18, 6}, {-14, -21, 7},
		}
		for _, tc := range cases {
			if got := m.GCD(tc.a, tc.b); got != tc.want {
				t.Errorf("GCD(%d, %d) = %d, want %d", tc.a, tc.b, got, tc.want)
			}
		}
	})
}

func TestDerivative(t *testing.T) {
	m := &MathOperations{}

	t.Run("valid derivatives", func(t *testing.T) {
		got, err := m.Derivative([]float64{3, 2, 5})
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		expected := []float64{2, 10}
		for i, v := range expected {
			if math.Abs(got[i]-v) > 0.001 {
				t.Errorf("Derivative([3,2,5])[%d] = %f, want %f", i, got[i], v)
			}
		}

		got, err = m.Derivative([]float64{0, 0, 0, 1})
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		expected = []float64{0, 0, 3}
		for i, v := range expected {
			if math.Abs(got[i]-v) > 0.001 {
				t.Errorf("Derivative([0,0,0,1])[%d] = %f, want %f", i, got[i], v)
			}
		}

		got, err = m.Derivative([]float64{7})
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if len(got) != 1 || got[0] != 0 {
			t.Errorf("Derivative([7]) = %v, want [0]", got)
		}
	})

	t.Run("empty polynomial", func(t *testing.T) {
		got, err := m.Derivative([]float64{})
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}
		if len(got) != 1 || got[0] != 0 {
			t.Errorf("Derivative([]) = %v, want [0]", got)
		}
	})

	t.Run("nil coefficients", func(t *testing.T) {
		_, err := m.Derivative(nil)
		if err == nil {
			t.Error("expected error for nil coefficients")
		}
	})
}
