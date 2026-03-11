#include "math_operations.h"

int add(int a, int b)
{
    return a + b;
}

int subtract(int a, int b)
{
    return a - b;
}

int multiply(int a, int b)
{
    return a * b;
}

double divide(double a, double b)
{
    if (b == 0.0)
    {
        return 0.0;
    }
    return a / b;
}

int power_int(int base, int exponent)
{
    if (exponent < 0)
    {
        return 0;
    }
    int result = 1;
    for (int i = 0; i < exponent; i++)
    {
        result *= base;
    }
    return result;
}

int factorial(int n)
{
    if (n < 0)
    {
        return -1;
    }
    if (n == 0 || n == 1)
    {
        return 1;
    }
    int result = 1;
    for (int i = 2; i <= n; i++)
    {
        result *= i;
    }
    return result;
}

int gcd(int a, int b)
{
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0)
    {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
