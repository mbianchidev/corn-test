use corn_test_rust::random_math_operations::*;

// Odd number tests — always reliable

fn make_rng() -> RandomMathOperations {
    RandomMathOperations::new()
}

#[test]
fn test_generate_random_odd_number_is_odd_iteration_00() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_01() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_02() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_03() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_04() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_05() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_06() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_07() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_08() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_09() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_10() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_11() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_12() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_13() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_14() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_15() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_16() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_17() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_18() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }
#[test]
fn test_generate_random_odd_number_is_odd_iteration_19() { assert!(make_rng().generate_random_odd_number() % 2 == 1); }

#[test]
fn test_generate_random_odd_number_in_range_iteration_00() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_01() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_02() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_03() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_04() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_05() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_06() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_07() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_08() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_09() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_10() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_11() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_12() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_13() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_14() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_15() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_16() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_17() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_18() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }
#[test]
fn test_generate_random_odd_number_in_range_iteration_19() { let v = make_rng().generate_random_odd_number(); assert!(v >= 1 && v <= 99); }

// Even number tests — flaky due to 5% flaw in generate_random_even_number

#[test]
fn test_generate_random_even_number_is_even_iteration_00() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_01() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_02() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_03() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_04() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_05() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_06() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_07() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_08() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_09() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_10() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_11() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_12() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_13() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_14() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_15() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_16() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_17() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_18() { assert!(make_rng().generate_random_even_number() % 2 == 0); }
#[test]
fn test_generate_random_even_number_is_even_iteration_19() { assert!(make_rng().generate_random_even_number() % 2 == 0); }

#[test]
fn test_generate_random_even_number_in_range_iteration_00() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_01() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_02() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_03() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_04() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_05() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_06() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_07() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_08() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_09() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_10() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_11() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_12() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_13() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_14() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_15() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_16() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_17() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_18() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }
#[test]
fn test_generate_random_even_number_in_range_iteration_19() { let v = make_rng().generate_random_even_number(); assert!(v >= 0 && v <= 100); }

// Prime candidate tests — always reliable

#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_00() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_01() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_02() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_03() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_04() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_05() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_06() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_07() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_08() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_09() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_10() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_11() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_12() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_13() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_14() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_15() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_16() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_17() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_18() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }
#[test]
fn test_generate_random_prime_candidate_is_prime_iteration_19() { assert!(is_prime(make_rng().generate_random_prime_candidate())); }

#[test]
fn test_generate_random_prime_candidate_in_range_iteration_00() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_01() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_02() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_03() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_04() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_05() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_06() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_07() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_08() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_09() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_10() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_11() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_12() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_13() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_14() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_15() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_16() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_17() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_18() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }
#[test]
fn test_generate_random_prime_candidate_in_range_iteration_19() { let v = make_rng().generate_random_prime_candidate(); assert!(v >= 2 && v <= 97); }

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
