#include "unity.h"
#include <stdio.h>
#include <string.h>
#include <setjmp.h>

struct UNITY_STORAGE_T Unity;

void UnityBegin(const char* filename)
{
    Unity.TestFile = filename;
    Unity.CurrentTestName = NULL;
    Unity.CurrentTestLineNumber = 0;
    Unity.NumberOfTests = 0;
    Unity.TestFailures = 0;
    Unity.TestIgnores = 0;
    Unity.CurrentTestFailed = 0;
    Unity.CurrentTestIgnored = 0;
}

int UnityEnd(void)
{
    printf("\n-----------------------\n");
    printf("%u Tests %u Failures %u Ignored\n",
           (unsigned)Unity.NumberOfTests,
           (unsigned)Unity.TestFailures,
           (unsigned)Unity.TestIgnores);

    if (Unity.TestFailures == 0U)
    {
        printf("OK\n");
    }
    else
    {
        printf("FAIL\n");
    }

    return (int)Unity.TestFailures;
}

void UnityConcludeTest(void)
{
    if (Unity.CurrentTestIgnored)
    {
        printf("%s:%u:%s:IGNORE\n",
               Unity.TestFile,
               (unsigned)Unity.CurrentTestLineNumber,
               Unity.CurrentTestName);
        Unity.TestIgnores++;
    }
    else if (Unity.CurrentTestFailed)
    {
        Unity.TestFailures++;
    }
    else
    {
        printf("%s:%u:%s:PASS\n",
               Unity.TestFile,
               (unsigned)Unity.CurrentTestLineNumber,
               Unity.CurrentTestName);
    }

    Unity.CurrentTestFailed = 0;
    Unity.CurrentTestIgnored = 0;
}

void UnityDefaultTestRun(void (*func)(void), const char* name, const int line)
{
    Unity.CurrentTestName = name;
    Unity.CurrentTestLineNumber = (UNITY_UINT)line;
    Unity.NumberOfTests++;
    Unity.CurrentTestFailed = 0;
    Unity.CurrentTestIgnored = 0;

    if (setjmp(Unity.AbortFrame) == 0)
    {
        setUp();
        func();
    }

    tearDown();
    UnityConcludeTest();
}

static void UnityPrintFail(const UNITY_UINT line)
{
    printf("%s:%u:%s:FAIL: ",
           Unity.TestFile,
           (unsigned)line,
           Unity.CurrentTestName);
}

void UnityAssertEqualNumber(const UNITY_INT expected,
                            const UNITY_INT actual,
                            const char* msg,
                            const UNITY_UINT lineNumber,
                            const UNITY_DISPLAY_STYLE_T style)
{
    (void)style;

    if (expected != actual)
    {
        Unity.CurrentTestFailed = 1;
        UnityPrintFail(lineNumber);
        printf("Expected %lld Was %lld", (long long)expected, (long long)actual);
        if (msg)
        {
            printf(": %s", msg);
        }
        printf("\n");
        longjmp(Unity.AbortFrame, 1);
    }
}

void UnityAssertFloatsWithin(const UNITY_FLOAT delta,
                             const UNITY_FLOAT expected,
                             const UNITY_FLOAT actual,
                             const char* msg,
                             const UNITY_UINT lineNumber)
{
    UNITY_FLOAT diff = actual - expected;
    if (diff < 0.0f) diff = -diff;

    if (diff > delta)
    {
        Unity.CurrentTestFailed = 1;
        UnityPrintFail(lineNumber);
        printf("Expected %f +/- %f Was %f", (double)expected, (double)delta, (double)actual);
        if (msg)
        {
            printf(": %s", msg);
        }
        printf("\n");
        longjmp(Unity.AbortFrame, 1);
    }
}

void UnityAssertNumbersWithin(const UNITY_INT delta,
                               const UNITY_INT expected,
                               const UNITY_INT actual,
                               const char* msg,
                               const UNITY_UINT lineNumber,
                               const UNITY_DISPLAY_STYLE_T style)
{
    (void)style;
    UNITY_INT diff = actual - expected;
    if (diff < 0) diff = -diff;

    if (diff > delta)
    {
        Unity.CurrentTestFailed = 1;
        UnityPrintFail(lineNumber);
        printf("Expected %lld +/- %lld Was %lld",
               (long long)expected, (long long)delta, (long long)actual);
        if (msg)
        {
            printf(": %s", msg);
        }
        printf("\n");
        longjmp(Unity.AbortFrame, 1);
    }
}

void UnityAssertTrue(const int condition,
                     const char* msg,
                     const UNITY_UINT lineNumber)
{
    if (!condition)
    {
        Unity.CurrentTestFailed = 1;
        UnityPrintFail(lineNumber);
        printf("Expected TRUE Was FALSE");
        if (msg)
        {
            printf(": %s", msg);
        }
        printf("\n");
        longjmp(Unity.AbortFrame, 1);
    }
}

void UnityAssertFalse(const int condition,
                      const char* msg,
                      const UNITY_UINT lineNumber)
{
    if (condition)
    {
        Unity.CurrentTestFailed = 1;
        UnityPrintFail(lineNumber);
        printf("Expected FALSE Was TRUE");
        if (msg)
        {
            printf(": %s", msg);
        }
        printf("\n");
        longjmp(Unity.AbortFrame, 1);
    }
}

void UnityAssertNull(const void* pointer,
                     const char* msg,
                     const UNITY_UINT lineNumber)
{
    if (pointer != NULL)
    {
        Unity.CurrentTestFailed = 1;
        UnityPrintFail(lineNumber);
        printf("Expected NULL");
        if (msg)
        {
            printf(": %s", msg);
        }
        printf("\n");
        longjmp(Unity.AbortFrame, 1);
    }
}

void UnityAssertNotNull(const void* pointer,
                        const char* msg,
                        const UNITY_UINT lineNumber)
{
    if (pointer == NULL)
    {
        Unity.CurrentTestFailed = 1;
        UnityPrintFail(lineNumber);
        printf("Expected Not NULL");
        if (msg)
        {
            printf(": %s", msg);
        }
        printf("\n");
        longjmp(Unity.AbortFrame, 1);
    }
}

void UnityFail(const char* msg, const UNITY_UINT lineNumber)
{
    Unity.CurrentTestFailed = 1;
    UnityPrintFail(lineNumber);
    if (msg)
    {
        printf("%s", msg);
    }
    printf("\n");
    longjmp(Unity.AbortFrame, 1);
}

void UnityIgnore(const char* msg, const UNITY_UINT lineNumber)
{
    Unity.CurrentTestIgnored = 1;
    (void)lineNumber;
    (void)msg;
    longjmp(Unity.AbortFrame, 1);
}
