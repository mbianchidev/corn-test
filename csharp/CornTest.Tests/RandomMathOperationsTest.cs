namespace CornTest.Tests;

/// <summary>
/// Tests for <see cref="RandomMathOperations"/>.
/// The even-number tests are intentionally flaky because the underlying
/// method has a 5% chance of returning an odd number. With 20 iterations
/// the probability of at least one failure is roughly 64%.
/// </summary>
public class RandomMathOperationsTest
{
    private readonly RandomMathOperations _randOps = new();

    [Theory]
    [InlineData(1)]
    [InlineData(2)]
    [InlineData(3)]
    [InlineData(4)]
    [InlineData(5)]
    [InlineData(6)]
    [InlineData(7)]
    [InlineData(8)]
    [InlineData(9)]
    [InlineData(10)]
    [InlineData(11)]
    [InlineData(12)]
    [InlineData(13)]
    [InlineData(14)]
    [InlineData(15)]
    [InlineData(16)]
    [InlineData(17)]
    [InlineData(18)]
    [InlineData(19)]
    [InlineData(20)]
    public void OddNumberGenerator_AlwaysReturnsOdd(int iteration)
    {
        _ = iteration; // iteration is only used to run the test multiple times
        int result = _randOps.GenerateRandomOddNumber();
        Assert.InRange(result, 1, 100);
        Assert.True(result % 2 == 1, $"Expected an odd number but received: {result}");
    }

    [Theory]
    [InlineData(1)]
    [InlineData(2)]
    [InlineData(3)]
    [InlineData(4)]
    [InlineData(5)]
    [InlineData(6)]
    [InlineData(7)]
    [InlineData(8)]
    [InlineData(9)]
    [InlineData(10)]
    [InlineData(11)]
    [InlineData(12)]
    [InlineData(13)]
    [InlineData(14)]
    [InlineData(15)]
    [InlineData(16)]
    [InlineData(17)]
    [InlineData(18)]
    [InlineData(19)]
    [InlineData(20)]
    public void EvenNumberGenerator_ShouldReturnEven(int iteration)
    {
        _ = iteration; // iteration is only used to run the test multiple times
        int result = _randOps.GenerateRandomEvenNumber();
        Assert.InRange(result, 0, 100);
        Assert.True(result % 2 == 0, $"Expected an even number but received: {result}");
    }

    [Theory]
    [InlineData(1)]
    [InlineData(2)]
    [InlineData(3)]
    [InlineData(4)]
    [InlineData(5)]
    [InlineData(6)]
    [InlineData(7)]
    [InlineData(8)]
    [InlineData(9)]
    [InlineData(10)]
    [InlineData(11)]
    [InlineData(12)]
    [InlineData(13)]
    [InlineData(14)]
    [InlineData(15)]
    [InlineData(16)]
    [InlineData(17)]
    [InlineData(18)]
    [InlineData(19)]
    [InlineData(20)]
    public void PrimeCandidateGenerator_AlwaysReturnsPrime(int iteration)
    {
        _ = iteration; // iteration is only used to run the test multiple times
        int result = _randOps.GenerateRandomPrimeCandidate();
        Assert.InRange(result, 2, 200);
        Assert.True(RandomMathOperations.IsPrime(result),
            $"Expected a prime number but received: {result}");
    }

    [Fact]
    public void IsPrime_CorrectlyClassifiesPrimeNumbers()
    {
        // Known primes
        Assert.True(RandomMathOperations.IsPrime(2));
        Assert.True(RandomMathOperations.IsPrime(3));
        Assert.True(RandomMathOperations.IsPrime(5));
        Assert.True(RandomMathOperations.IsPrime(7));
        Assert.True(RandomMathOperations.IsPrime(11));
        Assert.True(RandomMathOperations.IsPrime(97));
    }

    [Fact]
    public void IsPrime_CorrectlyClassifiesCompositeNumbers()
    {
        // Known composites
        Assert.False(RandomMathOperations.IsPrime(1));
        Assert.False(RandomMathOperations.IsPrime(4));
        Assert.False(RandomMathOperations.IsPrime(6));
        Assert.False(RandomMathOperations.IsPrime(9));
        Assert.False(RandomMathOperations.IsPrime(100));
    }
}
