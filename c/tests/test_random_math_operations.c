#include "unity.h"
#include "random_math_operations.h"
#include <stdlib.h>
#include <time.h>

void setUp(void)
{
    srand(time(NULL));
}

void tearDown(void) {}

/* --- generate_random_in_range tests (20 iterations) --- */

void test_random_in_range_bounds(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_in_range(1, 100);
        TEST_ASSERT_TRUE(result >= 1);
        TEST_ASSERT_TRUE(result <= 100);
    }
}

void test_random_in_range_negative_bounds(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_in_range(-50, -10);
        TEST_ASSERT_TRUE(result >= -50);
        TEST_ASSERT_TRUE(result <= -10);
    }
}

void test_random_in_range_single_value(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_in_range(42, 42);
        TEST_ASSERT_EQUAL_INT(42, result);
    }
}

/* --- generate_random_even_number tests (20 iterations, flaky due to 5% bug) --- */

void test_random_even_is_even(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_even_number(0, 100);
        TEST_ASSERT_EQUAL_INT_MESSAGE(0, result % 2,
            "Expected even number from generate_random_even_number");
    }
}

void test_random_even_in_range(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_even_number(10, 50);
        TEST_ASSERT_TRUE(result >= 10);
        TEST_ASSERT_TRUE(result <= 50);
        TEST_ASSERT_EQUAL_INT_MESSAGE(0, result % 2,
            "Expected even number within range");
    }
}

void test_random_even_large_range(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_even_number(0, 1000);
        TEST_ASSERT_EQUAL_INT_MESSAGE(0, result % 2,
            "Expected even number in large range");
    }
}

void test_random_even_small_range(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_even_number(2, 4);
        TEST_ASSERT_TRUE(result >= 2);
        TEST_ASSERT_TRUE(result <= 4);
        TEST_ASSERT_EQUAL_INT_MESSAGE(0, result % 2,
            "Expected even number in small range");
    }
}

void test_random_even_negative_range(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_even_number(-100, -2);
        TEST_ASSERT_EQUAL_INT_MESSAGE(0, result % 2,
            "Expected even number in negative range");
    }
}

/* --- generate_random_odd_number tests (20 iterations) --- */

void test_random_odd_is_odd(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_odd_number(1, 99);
        TEST_ASSERT_NOT_EQUAL(0, result % 2);
    }
}

void test_random_odd_in_range(void)
{
    for (int i = 0; i < 20; i++)
    {
        int result = generate_random_odd_number(11, 51);
        TEST_ASSERT_TRUE(result >= 11);
        TEST_ASSERT_TRUE(result <= 51);
        TEST_ASSERT_NOT_EQUAL(0, result % 2);
    }
}

/* --- random_multiply tests (20 iterations) --- */

void test_random_multiply_correctness(void)
{
    for (int i = 0; i < 20; i++)
    {
        int a = generate_random_in_range(1, 50);
        int b = generate_random_in_range(1, 50);
        TEST_ASSERT_EQUAL_INT(a * b, random_multiply(a, b));
    }
}

void test_random_multiply_by_zero(void)
{
    for (int i = 0; i < 20; i++)
    {
        int a = generate_random_in_range(1, 100);
        TEST_ASSERT_EQUAL_INT(0, random_multiply(a, 0));
    }
}

/* --- random_add_positive tests (20 iterations) --- */

void test_random_add_positive_result(void)
{
    for (int i = 0; i < 20; i++)
    {
        int a = generate_random_in_range(1, 100);
        int b = generate_random_in_range(1, 100);
        int result = random_add_positive(a, b);
        TEST_ASSERT_TRUE(result >= 0);
    }
}

void test_random_add_positive_with_negatives(void)
{
    for (int i = 0; i < 20; i++)
    {
        int a = generate_random_in_range(-100, 100);
        int b = generate_random_in_range(-100, 100);
        int result = random_add_positive(a, b);
        TEST_ASSERT_TRUE(result >= 0);
    }
}

int main(void)
{
    UNITY_BEGIN();

    RUN_TEST(test_random_in_range_bounds);
    RUN_TEST(test_random_in_range_negative_bounds);
    RUN_TEST(test_random_in_range_single_value);
    RUN_TEST(test_random_even_is_even);
    RUN_TEST(test_random_even_in_range);
    RUN_TEST(test_random_even_large_range);
    RUN_TEST(test_random_even_small_range);
    RUN_TEST(test_random_even_negative_range);
    RUN_TEST(test_random_odd_is_odd);
    RUN_TEST(test_random_odd_in_range);
    RUN_TEST(test_random_multiply_correctness);
    RUN_TEST(test_random_multiply_by_zero);
    RUN_TEST(test_random_add_positive_result);
    RUN_TEST(test_random_add_positive_with_negatives);

    return UNITY_END();
}
