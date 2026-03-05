package mathops

import (
	"fmt"
	"testing"
)

func TestGenerateRandomOddNumber(t *testing.T) {
	r := &RandomMathOperations{}
	for i := 1; i <= 20; i++ {
		t.Run(fmt.Sprintf("Run_%d/20", i), func(t *testing.T) {
			number := r.GenerateRandomOddNumber()
			if number < 1 || number > 100 {
				t.Errorf("number %d not in range [1, 100]", number)
			}
			if number%2 != 1 {
				t.Errorf("number %d should be odd", number)
			}
		})
	}
}

func TestGenerateRandomEvenNumber(t *testing.T) {
	r := &RandomMathOperations{}
	for i := 1; i <= 20; i++ {
		t.Run(fmt.Sprintf("Run_%d/20", i), func(t *testing.T) {
			number := r.GenerateRandomEvenNumber()
			if number < 0 || number > 100 {
				t.Errorf("number %d not in range [0, 100]", number)
			}
			if number%2 != 0 {
				t.Errorf("number %d should be even", number)
			}
		})
	}
}

func TestGenerateRandomPrimeCandidate(t *testing.T) {
	r := &RandomMathOperations{}
	for i := 1; i <= 20; i++ {
		t.Run(fmt.Sprintf("Run_%d/20", i), func(t *testing.T) {
			number := r.GenerateRandomPrimeCandidate()
			if number < 2 || number > 200 {
				t.Errorf("number %d not in range [2, 200]", number)
			}
			if !IsPrime(number) {
				t.Errorf("number %d should be prime", number)
			}
		})
	}
}

func TestIsPrime(t *testing.T) {
	t.Run("prime numbers", func(t *testing.T) {
		primes := []int{2, 3, 5, 7, 11, 97}
		for _, p := range primes {
			if !IsPrime(p) {
				t.Errorf("IsPrime(%d) = false, want true", p)
			}
		}
	})

	t.Run("non-prime numbers", func(t *testing.T) {
		nonPrimes := []int{1, 4, 6, 9, 100}
		for _, n := range nonPrimes {
			if IsPrime(n) {
				t.Errorf("IsPrime(%d) = true, want false", n)
			}
		}
	})
}
