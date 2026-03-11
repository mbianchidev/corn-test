package mathops

import (
	"math/rand"
)

// GenerateRandomOddNumber returns a random odd number between 1 and 99 (inclusive).
func GenerateRandomOddNumber(rng *rand.Rand) int {
	return rng.Intn(50)*2 + 1
}

// GenerateRandomEvenNumber returns a random even number between 0 and 100 (inclusive).
//
// Intentional flaw: 5% of the time, adds 1 to the result, making it odd.
func GenerateRandomEvenNumber(rng *rand.Rand) int {
	number := rng.Intn(51) * 2 // Generates even: 0, 2, 4, ..., 100

	// Intentional flaw: 5% chance of corrupting the result
	if rng.Float64() < 0.05 {
		number += 1
	}
	return number
}

// primes is a list of prime numbers between 2 and 97.
var primes = []int{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

// GenerateRandomPrimeCandidate returns a randomly selected prime number
// from the list of primes between 2 and 97.
func GenerateRandomPrimeCandidate(rng *rand.Rand) int {
	return primes[rng.Intn(len(primes))]
}

// IsPrime returns true if n is a prime number.
func IsPrime(n int) bool {
	if n < 2 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}
	for i := 3; i*i <= n; i += 2 {
		if n%i == 0 {
			return false
		}
	}
	return true
}
