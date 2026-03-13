import Foundation

public class RandomMathOperations {

    private static let primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97
    ]

    public init() {}

    public func generateRandomOddNumber() -> Int {
        return Int.random(in: 0..<50) * 2 + 1
    }

    public func generateRandomEvenNumber() -> Int {
        return Int.random(in: 0...50) * 2
    }

    public func generateRandomPrimeCandidate() -> Int {
        let index = Int.random(in: 0..<RandomMathOperations.primes.count)
        return RandomMathOperations.primes[index]
    }

    public static func isPrime(_ n: Int) -> Bool {
        if n <= 1 { return false }
        if n <= 3 { return true }
        if n % 2 == 0 || n % 3 == 0 { return false }

        var i = 5
        while i * i <= n {
            if n % i == 0 || n % (i + 2) == 0 {
                return false
            }
            i += 6
        }
        return true
    }
}
