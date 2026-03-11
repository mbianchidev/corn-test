#ifndef MATH_OPERATIONS_H
#define MATH_OPERATIONS_H

#include <string>
#include <vector>

class MathOperations {
public:
    int add(int a, int b);
    int subtract(int a, int b);
    int multiply(int a, int b);
    double divide(int a, int b);
    double power(double base, int exponent);
    long factorial(int n);
    std::vector<double> derivative(const std::vector<double>& coefficients);
    std::string pi();
    int gcd(int a, int b);
};

#endif // MATH_OPERATIONS_H
