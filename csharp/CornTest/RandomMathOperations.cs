namespace CornTest;

/// <summary>
/// Provides random number generation operations for testing flake detection.
/// The GenerateRandomEvenNumber method contains an intentional 5% flaw.
/// </summary>
public class RandomMathOperations
{
    private readonly Random _rng;

    public RandomMathOperations()
    {
        _rng = new Random();
    }

    public RandomMathOperations(int seed)
    {
        _rng = new Random(seed);
    }

    /// <summary>
    /// Produces a random odd integer in the range [1, 99].
    /// This method is reliable and always returns a valid odd number.
    /// </summary>
    public int GenerateRandomOddNumber()
    {
        // _rng.Next(50) yields 0..49, so result is 1,3,5,...,99
        return _rng.Next(50) * 2 + 1;
    }

    /// <summary>
    /// Produces a random even integer in the range [0, 100].
    /// <para>
    /// <b>Intentional flaw</b>: approximately 5% of invocations will
    /// corrupt the result by adding 1, yielding an odd number instead.
    /// </para>
    /// </summary>
    public int GenerateRandomEvenNumber()
    {
        // _rng.Next(51) yields 0..50, so result is 0,2,4,...,100
        int value = _rng.Next(51) * 2;

        // Intentional flaw: with ~5% probability, corrupt the even number
        if (_rng.NextDouble() < 0.05)
            value += 1;

        return value;
    }

    /// <summary>
    /// Selects a random prime from a curated list of primes up to 97.
    /// This method is reliable and always returns a valid prime.
    /// </summary>
    public int GenerateRandomPrimeCandidate()
    {
        int[] knownPrimes = { 2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97 };
        return knownPrimes[_rng.Next(knownPrimes.Length)];
    }

    /// <summary>
    /// Determines whether the specified integer is a prime number.
    /// Uses trial division with 6k +/- 1 optimisation.
    /// </summary>
    public static bool IsPrime(int n)
    {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (int d = 5; d * d <= n; d += 6)
        {
            if (n % d == 0 || n % (d + 2) == 0)
                return false;
        }
        return true;
    }
}
