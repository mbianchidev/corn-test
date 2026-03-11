#ifndef UNITY_FRAMEWORK_H
#define UNITY_FRAMEWORK_H

#include "unity_internals.h"

void UnityBegin(const char* filename);
int UnityEnd(void);

extern void setUp(void);
extern void tearDown(void);
void UnityConcludeTest(void);

void UnityDefaultTestRun(void (*func)(void), const char* name, const int line);

void UnityAssertEqualNumber(const UNITY_INT expected,
                            const UNITY_INT actual,
                            const char* msg,
                            const UNITY_UINT lineNumber,
                            const UNITY_DISPLAY_STYLE_T style);

void UnityAssertFloatsWithin(const UNITY_FLOAT delta,
                             const UNITY_FLOAT expected,
                             const UNITY_FLOAT actual,
                             const char* msg,
                             const UNITY_UINT lineNumber);

void UnityAssertNumbersWithin(const UNITY_INT delta,
                               const UNITY_INT expected,
                               const UNITY_INT actual,
                               const char* msg,
                               const UNITY_UINT lineNumber,
                               const UNITY_DISPLAY_STYLE_T style);

void UnityFail(const char* msg, const UNITY_UINT lineNumber);
void UnityIgnore(const char* msg, const UNITY_UINT lineNumber);

void UnityAssertTrue(const int condition,
                     const char* msg,
                     const UNITY_UINT lineNumber);

void UnityAssertFalse(const int condition,
                      const char* msg,
                      const UNITY_UINT lineNumber);

void UnityAssertNull(const void* pointer,
                     const char* msg,
                     const UNITY_UINT lineNumber);

void UnityAssertNotNull(const void* pointer,
                        const char* msg,
                        const UNITY_UINT lineNumber);

#define UNITY_BEGIN()                   UnityBegin(__FILE__)
#define UNITY_END()                     UnityEnd()

#define RUN_TEST(func)                  UnityDefaultTestRun(func, #func, __LINE__)

#define TEST_ASSERT_EQUAL_INT(expected, actual) \
    UnityAssertEqualNumber((UNITY_INT)(expected), (UNITY_INT)(actual), NULL, (UNITY_UINT)__LINE__, UNITY_DISPLAY_STYLE_INT)

#define TEST_ASSERT_EQUAL_INT_MESSAGE(expected, actual, msg) \
    UnityAssertEqualNumber((UNITY_INT)(expected), (UNITY_INT)(actual), (msg), (UNITY_UINT)__LINE__, UNITY_DISPLAY_STYLE_INT)

#define TEST_ASSERT_EQUAL(expected, actual) \
    TEST_ASSERT_EQUAL_INT((expected), (actual))

#define TEST_ASSERT_TRUE(condition) \
    UnityAssertTrue((int)(condition), NULL, (UNITY_UINT)__LINE__)

#define TEST_ASSERT_TRUE_MESSAGE(condition, msg) \
    UnityAssertTrue((int)(condition), (msg), (UNITY_UINT)__LINE__)

#define TEST_ASSERT_FALSE(condition) \
    UnityAssertFalse((int)(condition), NULL, (UNITY_UINT)__LINE__)

#define TEST_ASSERT_FALSE_MESSAGE(condition, msg) \
    UnityAssertFalse((int)(condition), (msg), (UNITY_UINT)__LINE__)

#define TEST_ASSERT_NULL(pointer) \
    UnityAssertNull((const void*)(pointer), NULL, (UNITY_UINT)__LINE__)

#define TEST_ASSERT_NOT_NULL(pointer) \
    UnityAssertNotNull((const void*)(pointer), NULL, (UNITY_UINT)__LINE__)

#define TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual) \
    UnityAssertFloatsWithin((UNITY_FLOAT)(delta), (UNITY_FLOAT)(expected), (UNITY_FLOAT)(actual), NULL, (UNITY_UINT)__LINE__)

#define TEST_ASSERT_INT_WITHIN(delta, expected, actual) \
    UnityAssertNumbersWithin((UNITY_INT)(delta), (UNITY_INT)(expected), (UNITY_INT)(actual), NULL, (UNITY_UINT)__LINE__, UNITY_DISPLAY_STYLE_INT)

#define TEST_FAIL_MESSAGE(msg) \
    UnityFail((msg), (UNITY_UINT)__LINE__)

#define TEST_FAIL() \
    TEST_FAIL_MESSAGE(NULL)

#define TEST_IGNORE_MESSAGE(msg) \
    UnityIgnore((msg), (UNITY_UINT)__LINE__)

#define TEST_IGNORE() \
    TEST_IGNORE_MESSAGE(NULL)

#define TEST_ASSERT_GREATER_OR_EQUAL_INT(threshold, actual) \
    UnityAssertTrue((int)((actual) >= (threshold)), "Expected greater or equal", (UNITY_UINT)__LINE__)

#define TEST_ASSERT_LESS_OR_EQUAL_INT(threshold, actual) \
    UnityAssertTrue((int)((actual) <= (threshold)), "Expected less or equal", (UNITY_UINT)__LINE__)

#define TEST_ASSERT_NOT_EQUAL(expected, actual) \
    UnityAssertTrue((int)((expected) != (actual)), "Expected not equal", (UNITY_UINT)__LINE__)

#endif /* UNITY_FRAMEWORK_H */
