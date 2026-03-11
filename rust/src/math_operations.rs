pub fn add(a: i64, b: i64) -> i64 {
    a + b
}

pub fn subtract(a: i64, b: i64) -> i64 {
    a - b
}

pub fn multiply(a: i64, b: i64) -> i64 {
    a * b
}

pub fn divide(a: i64, b: i64) -> Result<f64, String> {
    if b == 0 {
        return Err("Cannot divide by zero".to_string());
    }
    Ok(a as f64 / b as f64)
}

pub fn power(base: f64, exponent: i32) -> f64 {
    base.powi(exponent)
}

pub fn factorial(n: i64) -> Result<i64, String> {
    if n < 0 {
        return Err("Factorial is not defined for negative numbers".to_string());
    }
    let mut result: i64 = 1;
    for i in 2..=n {
        result *= i;
    }
    Ok(result)
}

pub fn derivative(coefficients: &[f64]) -> Vec<f64> {
    if coefficients.len() <= 1 {
        return vec![0.0];
    }
    coefficients
        .iter()
        .enumerate()
        .skip(1)
        .map(|(i, &c)| c * i as f64)
        .collect()
}

pub fn pi() -> &'static str {
    "3.1415926535897932384626433832795028841971"
}

pub fn gcd(a: i64, b: i64) -> i64 {
    let mut a = a.abs();
    let mut b = b.abs();
    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    a
}
