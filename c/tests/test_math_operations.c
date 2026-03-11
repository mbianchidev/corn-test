#include "unity.h"
#include "math_operations.h"

void setUp(void) {}
void tearDown(void) {}

void test_add_positive_numbers(void)
{
    TEST_ASSERT_EQUAL_INT(5, add(2, 3));
}

void test_add_negative_numbers(void)
{
    TEST_ASSERT_EQUAL_INT(-5, add(-2, -3));
}

void test_add_mixed_numbers(void)
{
    TEST_ASSERT_EQUAL_INT(1, add(-2, 3));
}

void test_add_zero(void)
{
    TEST_ASSERT_EQUAL_INT(7, add(7, 0));
}

void test_subtract_positive_numbers(void)
{
    TEST_ASSERT_EQUAL_INT(2, subtract(5, 3));
}

void test_subtract_negative_result(void)
{
    TEST_ASSERT_EQUAL_INT(-3, subtract(2, 5));
}

void test_subtract_negative_numbers(void)
{
    TEST_ASSERT_EQUAL_INT(1, subtract(-2, -3));
}

void test_multiply_positive_numbers(void)
{
    TEST_ASSERT_EQUAL_INT(15, multiply(3, 5));
}

void test_multiply_by_zero(void)
{
    TEST_ASSERT_EQUAL_INT(0, multiply(5, 0));
}

void test_multiply_negative_numbers(void)
{
    TEST_ASSERT_EQUAL_INT(6, multiply(-2, -3));
}

void test_divide_positive_numbers(void)
{
    TEST_ASSERT_FLOAT_WITHIN(0.001, 2.5, divide(5.0, 2.0));
}

void test_divide_by_zero(void)
{
    TEST_ASSERT_FLOAT_WITHIN(0.001, 0.0, divide(5.0, 0.0));
}

void test_divide_negative_numbers(void)
{
    TEST_ASSERT_FLOAT_WITHIN(0.001, 2.0, divide(-6.0, -3.0));
}

void test_power_int_positive_exponent(void)
{
    TEST_ASSERT_EQUAL_INT(8, power_int(2, 3));
}

void test_power_int_zero_exponent(void)
{
    TEST_ASSERT_EQUAL_INT(1, power_int(5, 0));
}

void test_power_int_one_exponent(void)
{
    TEST_ASSERT_EQUAL_INT(7, power_int(7, 1));
}

void test_power_int_negative_exponent(void)
{
    TEST_ASSERT_EQUAL_INT(0, power_int(2, -1));
}

void test_factorial_zero(void)
{
    TEST_ASSERT_EQUAL_INT(1, factorial(0));
}

void test_factorial_one(void)
{
    TEST_ASSERT_EQUAL_INT(1, factorial(1));
}

void test_factorial_positive(void)
{
    TEST_ASSERT_EQUAL_INT(120, factorial(5));
}

void test_factorial_negative(void)
{
    TEST_ASSERT_EQUAL_INT(-1, factorial(-1));
}

void test_gcd_basic(void)
{
    TEST_ASSERT_EQUAL_INT(6, gcd(12, 18));
}

void test_gcd_coprime(void)
{
    TEST_ASSERT_EQUAL_INT(1, gcd(7, 13));
}

void test_gcd_same_number(void)
{
    TEST_ASSERT_EQUAL_INT(5, gcd(5, 5));
}

void test_gcd_with_zero(void)
{
    TEST_ASSERT_EQUAL_INT(5, gcd(0, 5));
}

int main(void)
{
    UNITY_BEGIN();

    RUN_TEST(test_add_positive_numbers);
    RUN_TEST(test_add_negative_numbers);
    RUN_TEST(test_add_mixed_numbers);
    RUN_TEST(test_add_zero);
    RUN_TEST(test_subtract_positive_numbers);
    RUN_TEST(test_subtract_negative_result);
    RUN_TEST(test_subtract_negative_numbers);
    RUN_TEST(test_multiply_positive_numbers);
    RUN_TEST(test_multiply_by_zero);
    RUN_TEST(test_multiply_negative_numbers);
    RUN_TEST(test_divide_positive_numbers);
    RUN_TEST(test_divide_by_zero);
    RUN_TEST(test_divide_negative_numbers);
    RUN_TEST(test_power_int_positive_exponent);
    RUN_TEST(test_power_int_zero_exponent);
    RUN_TEST(test_power_int_one_exponent);
    RUN_TEST(test_power_int_negative_exponent);
    RUN_TEST(test_factorial_zero);
    RUN_TEST(test_factorial_one);
    RUN_TEST(test_factorial_positive);
    RUN_TEST(test_factorial_negative);
    RUN_TEST(test_gcd_basic);
    RUN_TEST(test_gcd_coprime);
    RUN_TEST(test_gcd_same_number);
    RUN_TEST(test_gcd_with_zero);

    return UNITY_END();
}
