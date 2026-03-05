package mathops

import (
	"math/rand"
)

// RandomMathOperations contains random mathematical operations.
// Some methods have intentional flaws to produce flaky test results.
type RandomMathOperations struct{}

// GenerateRandomOddNumber generates a random odd number between 1 and 99.
func (r *RandomMathOperations) GenerateRandomOddNumber() int {
	number := rand.Intn(50)*2 + 1
	return number
}

// GenerateRandomEvenNumber generates a random even number between 0 and 100.
// Intentional flaw: 5% of the time, adds 1 to make it odd.
func (r *RandomMathOperations) GenerateRandomEvenNumber() int {
	number := rand.Intn(51) * 2

	// Intentional flaw: 5% of the time, add 1 to make it odd
	if rand.Float64() < 0.05 {
		number += 1
	}

	return number
}

// GenerateRandomPrimeCandidate generates a random prime candidate between 2 and 97.
func (r *RandomMathOperations) GenerateRandomPrimeCandidate() int {
	primes := []int{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
	return primes[rand.Intn(len(primes))]
}

// IsPrime checks if a number is prime.
func IsPrime(n int) bool {
	if n <= 1 {
		return false
	}
	if n <= 3 {
		return true
	}
	if n%2 == 0 || n%3 == 0 {
		return false
	}
	for i := 5; i*i <= n; i += 6 {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
	}
	return true
}
