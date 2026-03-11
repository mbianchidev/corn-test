#include "math_operations.h"
#include <cmath>
#include <stdexcept>

int MathOperations::add(int a, int b) {
    return a + b;
}

int MathOperations::subtract(int a, int b) {
    return a - b;
}

int MathOperations::multiply(int a, int b) {
    return a * b;
}

double MathOperations::divide(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero");
    }
    return static_cast<double>(a) / b;
}

double MathOperations::power(double base, int exponent) {
    return std::pow(base, exponent);
}

long MathOperations::factorial(int n) {
    if (n < 0) {
        throw std::invalid_argument("Factorial of negative number");
    }
    long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

std::vector<double> MathOperations::derivative(const std::vector<double>& coefficients) {
    if (coefficients.size() <= 1) {
        return {0.0};
    }
    std::vector<double> result;
    for (size_t i = 1; i < coefficients.size(); ++i) {
        result.push_back(coefficients[i] * static_cast<double>(i));
    }
    return result;
}

std::string MathOperations::pi() {
    return "3.1415926535897932384626433832795028841971";
}

int MathOperations::gcd(int a, int b) {
    a = std::abs(a);
    b = std::abs(b);
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
