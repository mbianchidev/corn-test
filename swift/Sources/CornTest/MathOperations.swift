import Foundation

public enum MathError: Error {
    case divisionByZero
    case negativeFactorial
}

public class MathOperations {

    public init() {}

    public func add(_ a: Int, _ b: Int) -> Int {
        return a + b
    }

    public func subtract(_ a: Int, _ b: Int) -> Int {
        return a - b
    }

    public func multiply(_ a: Int, _ b: Int) -> Int {
        return a * b
    }

    public func divide(_ a: Int, _ b: Int) throws -> Double {
        if b == 0 {
            throw MathError.divisionByZero
        }
        return Double(a) / Double(b)
    }

    public func power(_ base: Double, _ exponent: Int) -> Double {
        return pow(base, Double(exponent))
    }

    public func factorial(_ n: Int) throws -> Int {
        if n < 0 {
            throw MathError.negativeFactorial
        }
        if n == 0 || n == 1 {
            return 1
        }
        var result = 1
        for i in 2...n {
            result *= i
        }
        return result
    }

    /// Computes the derivative of a polynomial represented by coefficients in ascending order.
    /// For example, [a, b, c] represents a + bx + cx², and its derivative is [b, 2c].
    public func derivative(_ coefficients: [Double]) -> [Double] {
        if coefficients.count <= 1 {
            return [0.0]
        }
        var result: [Double] = []
        for i in 1..<coefficients.count {
            result.append(coefficients[i] * Double(i))
        }
        return result
    }

    public func pi() -> String {
        return "3.1415926535897932384626433832795028841971"
    }

    public func gcd(_ a: Int, _ b: Int) -> Int {
        var a = abs(a)
        var b = abs(b)
        while b != 0 {
            let temp = b
            b = a % b
            a = temp
        }
        return a
    }
}
