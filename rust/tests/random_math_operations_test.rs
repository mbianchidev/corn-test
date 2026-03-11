use corn_test_rust::random_math_operations::*;

fn make_rng() -> RandomMathOperations {
    RandomMathOperations::new()
}

macro_rules! generate_iteration_tests {
    ($test_prefix:ident, $body:expr, $($i:literal),+ $(,)?) => {
        paste::paste! {
            $(
                #[test]
                fn [<$test_prefix _iteration_ $i>]() {
                    $body
                }
            )+
        }
    };
}

// Odd number tests — always reliable

generate_iteration_tests!(
    test_generate_random_odd_number_is_odd,
    { assert!(make_rng().generate_random_odd_number() % 2 == 1); },
    00, 01, 02, 03, 04, 05, 06, 07, 08, 09,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19
);

generate_iteration_tests!(
    test_generate_random_odd_number_in_range,
    { let v = make_rng().generate_random_odd_number(); assert!((1..=99).contains(&v)); },
    00, 01, 02, 03, 04, 05, 06, 07, 08, 09,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19
);

// Even number tests — flaky due to 5% flaw in generate_random_even_number

generate_iteration_tests!(
    test_generate_random_even_number_is_even,
    { assert!(make_rng().generate_random_even_number() % 2 == 0); },
    00, 01, 02, 03, 04, 05, 06, 07, 08, 09,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19
);

generate_iteration_tests!(
    test_generate_random_even_number_in_range,
    { let v = make_rng().generate_random_even_number(); assert!((0..=100).contains(&v)); },
    00, 01, 02, 03, 04, 05, 06, 07, 08, 09,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19
);

// Prime candidate tests — always reliable

generate_iteration_tests!(
    test_generate_random_prime_candidate_is_prime,
    { assert!(is_prime(make_rng().generate_random_prime_candidate())); },
    00, 01, 02, 03, 04, 05, 06, 07, 08, 09,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19
);

generate_iteration_tests!(
    test_generate_random_prime_candidate_in_range,
    { let v = make_rng().generate_random_prime_candidate(); assert!((2..=97).contains(&v)); },
    00, 01, 02, 03, 04, 05, 06, 07, 08, 09,
    10, 11, 12, 13, 14, 15, 16, 17, 18, 19
);

// is_prime deterministic tests

#[test]
fn test_is_prime_known_primes() {
    assert!(is_prime(2));
    assert!(is_prime(3));
    assert!(is_prime(5));
    assert!(is_prime(7));
    assert!(is_prime(11));
    assert!(is_prime(97));
}

#[test]
fn test_is_prime_known_non_primes() {
    assert!(!is_prime(1));
    assert!(!is_prime(4));
    assert!(!is_prime(6));
    assert!(!is_prime(9));
    assert!(!is_prime(100));
}

#[test]
fn test_is_prime_edge_cases() {
    assert!(!is_prime(0));
    assert!(!is_prime(-5));
}
