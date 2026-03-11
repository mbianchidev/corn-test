#ifndef UNITY_INTERNALS_H
#define UNITY_INTERNALS_H

#include <stdio.h>
#include <string.h>
#include <setjmp.h>

typedef unsigned short UNITY_UINT16;
typedef unsigned int UNITY_UINT;
typedef int UNITY_INT;
typedef long long UNITY_INT64;
typedef unsigned long long UNITY_UINT64;
typedef float UNITY_FLOAT;
typedef double UNITY_DOUBLE;

typedef enum {
    UNITY_DISPLAY_STYLE_INT = 0,
    UNITY_DISPLAY_STYLE_UINT,
    UNITY_DISPLAY_STYLE_HEX8,
    UNITY_DISPLAY_STYLE_HEX16,
    UNITY_DISPLAY_STYLE_HEX32
} UNITY_DISPLAY_STYLE_T;

struct UNITY_STORAGE_T {
    const char* TestFile;
    const char* CurrentTestName;
    UNITY_UINT CurrentTestLineNumber;
    UNITY_UINT NumberOfTests;
    UNITY_UINT TestFailures;
    UNITY_UINT TestIgnores;
    UNITY_UINT CurrentTestFailed;
    UNITY_UINT CurrentTestIgnored;
    jmp_buf AbortFrame;
};

extern struct UNITY_STORAGE_T Unity;

#endif /* UNITY_INTERNALS_H */
