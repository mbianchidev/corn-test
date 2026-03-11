package mathops

import (
	"fmt"
	"math/rand"
	"testing"
	"time"
)

func TestGenerateRandomOddNumber(t *testing.T) {
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := 0; i < 20; i++ {
		t.Run(fmt.Sprintf("iteration_%d", i), func(t *testing.T) {
			number := GenerateRandomOddNumber(rng)
			if number < 1 || number > 99 {
				t.Errorf("iteration %d: odd number %d out of range [1, 99]", i, number)
			}
			if number%2 == 0 {
				t.Errorf("iteration %d: expected odd, got %d", i, number)
			}
		})
	}
}

// Flaky: fails ~50% of the time due to the intentional 5% flaw in GenerateRandomEvenNumber.
func TestGenerateRandomEvenNumber(t *testing.T) {
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := 0; i < 20; i++ {
		t.Run(fmt.Sprintf("iteration_%d", i), func(t *testing.T) {
			number := GenerateRandomEvenNumber(rng)
			if number < 0 || number > 101 {
				t.Errorf("iteration %d: even number %d out of range [0, 100]", i, number)
			}
			if number%2 != 0 {
				t.Errorf("iteration %d: expected even, got %d", i, number)
			}
		})
	}
}

func TestGenerateRandomPrimeCandidate(t *testing.T) {
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := 0; i < 20; i++ {
		t.Run(fmt.Sprintf("iteration_%d", i), func(t *testing.T) {
			number := GenerateRandomPrimeCandidate(rng)
			if number < 2 || number > 97 {
				t.Errorf("iteration %d: prime candidate %d out of range [2, 97]", i, number)
			}
			if !IsPrime(number) {
				t.Errorf("iteration %d: expected prime, got %d", i, number)
			}
		})
	}
}

func TestIsPrime(t *testing.T) {
	tests := []struct {
		name     string
		n        int
		expected bool
	}{
		{"negative", -1, false},
		{"zero", 0, false},
		{"one", 1, false},
		{"two", 2, true},
		{"three", 3, true},
		{"four", 4, false},
		{"seventeen", 17, true},
		{"ninety-seven", 97, true},
		{"hundred", 100, false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsPrime(tt.n)
			if result != tt.expected {
				t.Errorf("IsPrime(%d) = %v, want %v", tt.n, result, tt.expected)
			}
		})
	}
}
