import XCTest
@testable import CornTest

final class RandomMathOperationsTests: XCTestCase {

    var rng: RandomMathOperations!

    override func setUp() {
        super.setUp()
        rng = RandomMathOperations()
    }

    // MARK: - Odd Number Tests

    func testOddNumberIsOdd() {
        for i in 0..<20 {
            let number = rng.generateRandomOddNumber()
            XCTAssertEqual(number % 2, 1, "Iteration \(i): Expected odd, got \(number)")
        }
    }

    func testOddNumberInRange() {
        for i in 0..<20 {
            let number = rng.generateRandomOddNumber()
            XCTAssertTrue(number >= 1 && number <= 99, "Iteration \(i): Expected 1-99, got \(number)")
        }
    }

    // MARK: - Even Number Tests

    func testEvenNumberIsEven() {
        for i in 0..<20 {
            let number = rng.generateRandomEvenNumber()
            XCTAssertEqual(number % 2, 0, "Iteration \(i): Expected even, got \(number)")
        }
    }

    func testEvenNumberInRange() {
        for i in 0..<20 {
            let number = rng.generateRandomEvenNumber()
            XCTAssertTrue(number >= 0 && number <= 100, "Iteration \(i): Expected 0-100, got \(number)")
        }
    }

    // MARK: - Prime Candidate Tests

    func testPrimeCandidateIsPrime() {
        for i in 0..<20 {
            let number = rng.generateRandomPrimeCandidate()
            XCTAssertTrue(RandomMathOperations.isPrime(number), "Iteration \(i): Expected prime, got \(number)")
        }
    }

    func testPrimeCandidateInRange() {
        for i in 0..<20 {
            let number = rng.generateRandomPrimeCandidate()
            XCTAssertTrue(number >= 2 && number <= 97, "Iteration \(i): Expected 2-97, got \(number)")
        }
    }

    // MARK: - isPrime Tests

    func testIsPrimeWithKnownPrimes() {
        let knownPrimes = [2, 3, 5, 7, 11, 97]
        for prime in knownPrimes {
            XCTAssertTrue(RandomMathOperations.isPrime(prime), "\(prime) should be prime")
        }
    }

    func testIsPrimeWithKnownNonPrimes() {
        let nonPrimes = [1, 4, 6, 9, 100]
        for n in nonPrimes {
            XCTAssertFalse(RandomMathOperations.isPrime(n), "\(n) should not be prime")
        }
    }
}
