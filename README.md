# corn-test
Corn: the flakes detection agentic workflow

## Java Sample Application with Flaky Tests

This repository contains a sample Java application built with Maven, featuring mathematical operations and intentionally flaky tests for testing flake detection systems.

### Project Structure

```
corn-test/
├── pom.xml                           # Maven configuration
├── src/
│   ├── main/java/com/corntest/
│   │   ├── MathOperations.java       # 7 deterministic math functions
│   │   └── RandomMathOperations.java # 3 probabilistic functions
│   └── test/java/com/corntest/
│       ├── MathOperationsTest.java       # Reliable tests (always pass)
│       └── RandomMathOperationsTest.java # Flaky tests
```

### Features

#### MathOperations Class (7 Functions)
Deterministic mathematical operations that always produce consistent results:
1. `add(int a, int b)` - Addition
2. `subtract(int a, int b)` - Subtraction
3. `multiply(int a, int b)` - Multiplication
4. `divide(int a, int b)` - Division with zero-check
5. `power(double base, int exponent)` - Exponentiation
6. `factorial(int n)` - Factorial calculation
7. `gcd(int a, int b)` - Greatest Common Divisor

#### RandomMathOperations Class (3 Probabilistic Functions)
Functions designed to produce flaky test results:
1. `generateRandomOddNumber()` - **Fails ~25% of the time**
   - Should return odd numbers but occasionally returns even numbers
2. `generateRandomEvenNumber()` - **Fails ~50% of the time**
   - Should return even numbers but occasionally returns odd numbers
3. `generateRandomPrimeCandidate()` - **Fails ~75% of the time**
   - Should return prime numbers but frequently returns composite numbers

### Building and Testing

```bash
# Compile the project
mvn clean compile

# Run tests (will show flaky behavior)
mvn test

# Run tests multiple times to observe flakiness
mvn clean test && mvn test && mvn test
```

### Test Results

The flaky tests use `@RepeatedTest(20)` to run each test 20 times, demonstrating the probabilistic failure rates:

- **MathOperationsTest**: 11 tests, all deterministic (always pass)
- **RandomMathOperationsTest**: 3 flaky tests with varying failure rates

### Purpose

This project is designed for testing flake detection systems and CI/CD pipelines. The intentionally flaky tests help validate:
- Flake detection algorithms
- Test retry mechanisms
- CI/CD resilience strategies
- Test reliability metrics 
