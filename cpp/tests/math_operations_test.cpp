#include <gtest/gtest.h>
#include "math_operations.h"

class MathOperationsTest : public ::testing::Test {
protected:
    MathOperations math;
};

// Add tests
TEST_F(MathOperationsTest, AddPositiveNumbers) {
    EXPECT_EQ(math.add(2, 3), 5);
    EXPECT_EQ(math.add(40, 60), 100);
}

TEST_F(MathOperationsTest, AddNegativeNumbers) {
    EXPECT_EQ(math.add(-2, -3), -5);
    EXPECT_EQ(math.add(5, -5), 0);
}

// Subtract tests
TEST_F(MathOperationsTest, Subtract) {
    EXPECT_EQ(math.subtract(5, 3), 2);
    EXPECT_EQ(math.subtract(3, 5), -2);
}

// Multiply tests
TEST_F(MathOperationsTest, Multiply) {
    EXPECT_EQ(math.multiply(3, 4), 12);
    EXPECT_EQ(math.multiply(-3, 4), -12);
}

// Divide tests
TEST_F(MathOperationsTest, Divide) {
    EXPECT_DOUBLE_EQ(math.divide(6, 3), 2.0);
    EXPECT_DOUBLE_EQ(math.divide(5, 2), 2.5);
}

TEST_F(MathOperationsTest, DivideByZero) {
    EXPECT_THROW(math.divide(1, 0), std::invalid_argument);
}

// Power tests
TEST_F(MathOperationsTest, Power) {
    EXPECT_DOUBLE_EQ(math.power(2, 3), 8.0);
    EXPECT_DOUBLE_EQ(math.power(5, 0), 1.0);
    EXPECT_DOUBLE_EQ(math.power(2, -2), 0.25);
}

// Factorial tests
TEST_F(MathOperationsTest, Factorial) {
    EXPECT_EQ(math.factorial(0), 1);
    EXPECT_EQ(math.factorial(5), 120);
}

TEST_F(MathOperationsTest, FactorialNegative) {
    EXPECT_THROW(math.factorial(-1), std::invalid_argument);
}

// Pi tests
TEST_F(MathOperationsTest, Pi) {
    std::string result = math.pi();
    EXPECT_EQ(result, "3.1415926535897932384626433832795028841971");
    EXPECT_EQ(result.size(), 42u);
}

// GCD tests
TEST_F(MathOperationsTest, Gcd) {
    EXPECT_EQ(math.gcd(10, 15), 5);
    EXPECT_EQ(math.gcd(48, 18), 6);
    EXPECT_EQ(math.gcd(17, 19), 1);
}

TEST_F(MathOperationsTest, GcdNegative) {
    EXPECT_EQ(math.gcd(-10, 15), 5);
    EXPECT_EQ(math.gcd(10, -15), 5);
    EXPECT_EQ(math.gcd(-10, -15), 5);
}

// Derivative tests
TEST_F(MathOperationsTest, DerivativeQuadratic) {
    std::vector<double> result = math.derivative({3.0, 2.0, 1.0});
    ASSERT_EQ(result.size(), 2u);
    EXPECT_DOUBLE_EQ(result[0], 2.0);
    EXPECT_DOUBLE_EQ(result[1], 2.0);
}

TEST_F(MathOperationsTest, DerivativeCubic) {
    std::vector<double> result = math.derivative({1.0, 0.0, 3.0, 4.0});
    ASSERT_EQ(result.size(), 3u);
    EXPECT_DOUBLE_EQ(result[0], 0.0);
    EXPECT_DOUBLE_EQ(result[1], 6.0);
    EXPECT_DOUBLE_EQ(result[2], 12.0);
}

TEST_F(MathOperationsTest, DerivativeConstant) {
    std::vector<double> result = math.derivative({5.0});
    ASSERT_EQ(result.size(), 1u);
    EXPECT_DOUBLE_EQ(result[0], 0.0);
}

TEST_F(MathOperationsTest, DerivativeLinear) {
    std::vector<double> result = math.derivative({2.0, 3.0});
    ASSERT_EQ(result.size(), 1u);
    EXPECT_DOUBLE_EQ(result[0], 3.0);
}

TEST_F(MathOperationsTest, DerivativeEmpty) {
    std::vector<double> result = math.derivative({});
    ASSERT_EQ(result.size(), 1u);
    EXPECT_DOUBLE_EQ(result[0], 0.0);
}
