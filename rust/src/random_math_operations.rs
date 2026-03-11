use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

const PRIMES: [i32; 25] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
    97,
];

pub struct RandomMathOperations {
    rng: StdRng,
}

impl RandomMathOperations {
    pub fn new() -> Self {
        Self {
            rng: StdRng::from_entropy(),
        }
    }

    pub fn with_seed(seed: u64) -> Self {
        Self {
            rng: StdRng::seed_from_u64(seed),
        }
    }

    /// Generates a random odd number between 1 and 99 inclusive. Always correct.
    pub fn generate_random_odd_number(&mut self) -> i32 {
        self.rng.gen_range(0..50) * 2 + 1
    }

    /// Generates a random even number between 0 and 100 inclusive.
    /// Has a 5% chance of adding 1, making the result odd.
    pub fn generate_random_even_number(&mut self) -> i32 {
        let mut number = self.rng.gen_range(0..51) * 2; // 0, 2, 4, ..., 100
        if self.rng.gen::<f64>() < 0.05 {
            number += 1; // 5% chance to make it odd
        }
        number
    }

    /// Generates a random prime candidate from the list of primes 2-97. Always correct.
    pub fn generate_random_prime_candidate(&mut self) -> i32 {
        let index = self.rng.gen_range(0..PRIMES.len());
        PRIMES[index]
    }
}

pub fn is_prime(n: i32) -> bool {
    if n < 2 {
        return false;
    }
    if n < 4 {
        return true;
    }
    if n % 2 == 0 || n % 3 == 0 {
        return false;
    }
    let mut i = 5;
    while i * i <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    true
}
