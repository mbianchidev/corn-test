use corn_test_rust::math_operations::*;

#[test]
fn test_add_positive_numbers() {
    assert_eq!(add(2, 3), 5);
    assert_eq!(add(40, 60), 100);
}

#[test]
fn test_add_negative_numbers() {
    assert_eq!(add(-2, -3), -5);
    assert_eq!(add(5, -5), 0);
}

#[test]
fn test_subtract() {
    assert_eq!(subtract(5, 3), 2);
    assert_eq!(subtract(3, 5), -2);
    assert_eq!(subtract(10, 10), 0);
}

#[test]
fn test_multiply() {
    assert_eq!(multiply(2, 3), 6);
    assert_eq!(multiply(-2, 3), -6);
    assert_eq!(multiply(0, 100), 0);
}

#[test]
fn test_divide() {
    assert!((divide(6, 3).unwrap() - 2.0).abs() < 0.001);
    assert!((divide(5, 2).unwrap() - 2.5).abs() < 0.001);
    assert!((divide(6, -3).unwrap() - (-2.0)).abs() < 0.001);
}

#[test]
fn test_divide_by_zero() {
    assert!(divide(1, 0).is_err());
}

#[test]
fn test_power() {
    assert!((power(2.0, 3) - 8.0).abs() < f64::EPSILON);
    assert!((power(5.0, 0) - 1.0).abs() < f64::EPSILON);
    assert!((power(2.0, -2) - 0.25).abs() < f64::EPSILON);
}

#[test]
fn test_factorial() {
    assert_eq!(factorial(0).unwrap(), 1);
    assert_eq!(factorial(1).unwrap(), 1);
    assert_eq!(factorial(2).unwrap(), 2);
    assert_eq!(factorial(3).unwrap(), 6);
    assert_eq!(factorial(4).unwrap(), 24);
    assert_eq!(factorial(5).unwrap(), 120);
}

#[test]
fn test_factorial_negative() {
    assert!(factorial(-1).is_err());
}

#[test]
fn test_pi() {
    assert_eq!(pi(), "3.1415926535897932384626433832795028841971");
}

#[test]
fn test_gcd() {
    assert_eq!(gcd(1, 1), 1);
    assert_eq!(gcd(10, 15), 5);
    assert_eq!(gcd(48, 18), 6);
    assert_eq!(gcd(17, 19), 1);
}

#[test]
fn test_gcd_negative() {
    assert_eq!(gcd(-10, 15), 5);
    assert_eq!(gcd(48, -18), 6);
    assert_eq!(gcd(-14, -21), 7);
}

#[test]
fn test_derivative() {
    assert_eq!(derivative(&[3.0, 2.0, 5.0]), vec![2.0, 10.0]);
    assert_eq!(derivative(&[0.0, 0.0, 0.0, 1.0]), vec![0.0, 0.0, 3.0]);
    assert_eq!(derivative(&[7.0]), vec![0.0]);
}

#[test]
fn test_derivative_empty() {
    assert_eq!(derivative(&[]), vec![0.0]);
}
