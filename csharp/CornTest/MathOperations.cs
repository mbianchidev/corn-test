namespace CornTest;

/// <summary>
/// Provides deterministic mathematical operations for testing purposes.
/// All methods in this class produce predictable, repeatable results.
/// </summary>
public class MathOperations
{
    /// <summary>Computes the sum of two integers.</summary>
    public int Add(int a, int b) => a + b;

    /// <summary>Computes the difference of two integers.</summary>
    public int Subtract(int a, int b) => a - b;

    /// <summary>Computes the product of two integers.</summary>
    public int Multiply(int a, int b) => a * b;

    /// <summary>
    /// Computes the quotient of two integers as a double.
    /// </summary>
    /// <exception cref="DivideByZeroException">Thrown when the divisor is zero.</exception>
    public double Divide(int a, int b)
    {
        if (b == 0)
            throw new DivideByZeroException("Cannot divide by zero");
        return (double)a / b;
    }

    /// <summary>Raises a base value to the given integer exponent.</summary>
    public double Power(double baseVal, int exponent) => Math.Pow(baseVal, exponent);

    /// <summary>
    /// Computes n! iteratively.
    /// </summary>
    /// <exception cref="ArgumentException">Thrown when n is negative.</exception>
    public long Factorial(int n)
    {
        if (n < 0)
            throw new ArgumentException("Factorial is undefined for negative integers");
        if (n <= 1)
            return 1L;
        long accumulator = 1L;
        for (int idx = 2; idx <= n; idx++)
            accumulator *= idx;
        return accumulator;
    }

    /// <summary>
    /// Computes the derivative of a polynomial whose coefficients are given
    /// in ascending order of degree.
    /// For example, {3, 2, 5} represents 3 + 2x + 5x^2, and the derivative
    /// is {2, 10} representing 2 + 10x.
    /// </summary>
    /// <exception cref="ArgumentNullException">Thrown when coefficients is null.</exception>
    public double[] Derivative(double[] coefficients)
    {
        ArgumentNullException.ThrowIfNull(coefficients);
        if (coefficients.Length <= 1)
            return new double[] { 0.0 };
        var derived = new double[coefficients.Length - 1];
        for (int i = 1; i < coefficients.Length; i++)
            derived[i - 1] = coefficients[i] * i;
        return derived;
    }

    /// <summary>Returns pi to 40 decimal places as a string.</summary>
    public string Pi() => "3.1415926535897932384626433832795028841971";

    /// <summary>
    /// Computes the greatest common divisor via the Euclidean algorithm.
    /// Negative inputs are handled by taking absolute values first.
    /// </summary>
    public int Gcd(int a, int b)
    {
        a = Math.Abs(a);
        b = Math.Abs(b);
        while (b != 0)
        {
            int remainder = a % b;
            a = b;
            b = remainder;
        }
        return a;
    }
}
