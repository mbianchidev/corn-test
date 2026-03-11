import XCTest
@testable import CornTest

final class MathOperationsTests: XCTestCase {

    var math: MathOperations!

    override func setUp() {
        super.setUp()
        math = MathOperations()
    }

    // MARK: - Add

    func testAddPositiveNumbers() {
        XCTAssertEqual(math.add(2, 3), 5)
    }

    func testAddNegativeNumbers() {
        XCTAssertEqual(math.add(-2, -3), -5)
    }

    func testAddMixedNumbers() {
        XCTAssertEqual(math.add(-2, 3), 1)
    }

    // MARK: - Subtract

    func testSubtract() {
        XCTAssertEqual(math.subtract(5, 3), 2)
    }

    func testSubtractNegativeResult() {
        XCTAssertEqual(math.subtract(3, 5), -2)
    }

    // MARK: - Multiply

    func testMultiply() {
        XCTAssertEqual(math.multiply(4, 5), 20)
    }

    func testMultiplyByZero() {
        XCTAssertEqual(math.multiply(4, 0), 0)
    }

    // MARK: - Divide

    func testDivide() throws {
        let result = try math.divide(10, 3)
        XCTAssertEqual(result, 3.3333333333333335, accuracy: 1e-10)
    }

    func testDivideByZero() {
        XCTAssertThrowsError(try math.divide(10, 0)) { error in
            XCTAssertEqual(error as? MathError, MathError.divisionByZero)
        }
    }

    // MARK: - Power

    func testPower() {
        XCTAssertEqual(math.power(2.0, 10), 1024.0, accuracy: 1e-10)
    }

    func testPowerOfZero() {
        XCTAssertEqual(math.power(2.0, 0), 1.0, accuracy: 1e-10)
    }

    // MARK: - Factorial

    func testFactorial() throws {
        XCTAssertEqual(try math.factorial(0), 1)
        XCTAssertEqual(try math.factorial(1), 1)
        XCTAssertEqual(try math.factorial(5), 120)
        XCTAssertEqual(try math.factorial(10), 3628800)
    }

    func testFactorialNegative() {
        XCTAssertThrowsError(try math.factorial(-1)) { error in
            XCTAssertEqual(error as? MathError, MathError.negativeFactorial)
        }
    }

    // MARK: - Pi

    func testPi() {
        let result = math.pi()
        XCTAssertTrue(result.hasPrefix("3.14159265"))
        XCTAssertEqual(result, "3.1415926535897932384626433832795028841971")
    }

    // MARK: - GCD

    func testGcd() {
        XCTAssertEqual(math.gcd(12, 8), 4)
        XCTAssertEqual(math.gcd(100, 75), 25)
        XCTAssertEqual(math.gcd(7, 13), 1)
    }

    func testGcdNegative() {
        XCTAssertEqual(math.gcd(-12, 8), 4)
        XCTAssertEqual(math.gcd(12, -8), 4)
        XCTAssertEqual(math.gcd(-12, -8), 4)
    }

    // MARK: - Derivative

    func testDerivative() {
        // 3 + 2x + x² → 2 + 2x
        let result = math.derivative([3.0, 2.0, 1.0])
        XCTAssertEqual(result.count, 2)
        XCTAssertEqual(result[0], 2.0, accuracy: 1e-10)
        XCTAssertEqual(result[1], 2.0, accuracy: 1e-10)
    }

    func testDerivativeConstant() {
        // Derivative of a constant is 0
        let result = math.derivative([5.0])
        XCTAssertEqual(result, [0.0])
    }

    func testDerivativeEmpty() {
        let result = math.derivative([])
        XCTAssertEqual(result, [0.0])
    }
}
