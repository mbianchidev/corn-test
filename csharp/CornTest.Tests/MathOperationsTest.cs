namespace CornTest.Tests;

/// <summary>
/// Deterministic tests for <see cref="MathOperations"/>.
/// Every test here should pass on every run.
/// </summary>
public class MathOperationsTest
{
    private readonly MathOperations _ops = new();

    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(40, 60, 100)]
    [InlineData(-2, -3, -5)]
    [InlineData(5, -5, 0)]
    public void Add_ReturnsExpectedSum(int a, int b, int expected)
    {
        Assert.Equal(expected, _ops.Add(a, b));
    }

    [Theory]
    [InlineData(5, 3, 2)]
    [InlineData(3, 5, -2)]
    [InlineData(10, 10, 0)]
    public void Subtract_ReturnsExpectedDifference(int a, int b, int expected)
    {
        Assert.Equal(expected, _ops.Subtract(a, b));
    }

    [Theory]
    [InlineData(2, 3, 6)]
    [InlineData(-2, 3, -6)]
    [InlineData(0, 100, 0)]
    public void Multiply_ReturnsExpectedProduct(int a, int b, int expected)
    {
        Assert.Equal(expected, _ops.Multiply(a, b));
    }

    [Theory]
    [InlineData(6, 3, 2.0)]
    [InlineData(5, 2, 2.5)]
    [InlineData(6, -3, -2.0)]
    public void Divide_ReturnsExpectedQuotient(int a, int b, double expected)
    {
        Assert.Equal(expected, _ops.Divide(a, b), precision: 3);
    }

    [Fact]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        Assert.Throws<DivideByZeroException>(() => _ops.Divide(5, 0));
    }

    [Theory]
    [InlineData(2.0, 3, 8.0)]
    [InlineData(5.0, 0, 1.0)]
    [InlineData(2.0, -2, 0.25)]
    public void Power_ReturnsExpectedResult(double baseVal, int exp, double expected)
    {
        Assert.Equal(expected, _ops.Power(baseVal, exp), precision: 3);
    }

    [Theory]
    [InlineData(0, 1L)]
    [InlineData(1, 1L)]
    [InlineData(2, 2L)]
    [InlineData(3, 6L)]
    [InlineData(4, 24L)]
    [InlineData(5, 120L)]
    public void Factorial_ReturnsExpectedValue(int n, long expected)
    {
        Assert.Equal(expected, _ops.Factorial(n));
    }

    [Fact]
    public void Factorial_NegativeInput_ThrowsArgumentException()
    {
        Assert.Throws<ArgumentException>(() => _ops.Factorial(-1));
    }

    [Fact]
    public void Pi_ReturnsFortyDecimalDigits()
    {
        string expected = "3.1415926535897932384626433832795028841971";
        Assert.Equal(expected, _ops.Pi());
    }

    [Theory]
    [InlineData(1, 1, 1)]
    [InlineData(10, 15, 5)]
    [InlineData(48, 18, 6)]
    [InlineData(17, 19, 1)]
    public void Gcd_ReturnsExpectedValue(int a, int b, int expected)
    {
        Assert.Equal(expected, _ops.Gcd(a, b));
    }

    [Theory]
    [InlineData(-10, 15, 5)]
    [InlineData(48, -18, 6)]
    [InlineData(-14, -21, 7)]
    public void Gcd_NegativeInputs_ReturnsExpectedValue(int a, int b, int expected)
    {
        Assert.Equal(expected, _ops.Gcd(a, b));
    }

    [Fact]
    public void Derivative_ReturnsCorrectCoefficients()
    {
        // d/dx(3 + 2x + 5x^2) = 2 + 10x
        Assert.Equal(new double[] { 2, 10 }, _ops.Derivative(new double[] { 3, 2, 5 }));
        // d/dx(x^3) = 3x^2
        Assert.Equal(new double[] { 0, 0, 3 }, _ops.Derivative(new double[] { 0, 0, 0, 1 }));
        // d/dx(7) = 0
        Assert.Equal(new double[] { 0.0 }, _ops.Derivative(new double[] { 7 }));
    }

    [Fact]
    public void Derivative_EmptyInput_ReturnsZero()
    {
        Assert.Equal(new double[] { 0.0 }, _ops.Derivative(Array.Empty<double>()));
    }

    [Fact]
    public void Derivative_NullInput_ThrowsArgumentNullException()
    {
        Assert.Throws<ArgumentNullException>(() => _ops.Derivative(null!));
    }
}
