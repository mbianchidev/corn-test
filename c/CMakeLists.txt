cmake_minimum_required(VERSION 3.14)
project(corn-test-c LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Unity test framework from vendor directory
add_library(unity STATIC
    vendor/unity/unity.c
)
target_include_directories(unity PUBLIC
    vendor/unity
)

# Math operations library
add_library(math_operations STATIC
    src/math_operations.c
)
target_include_directories(math_operations PUBLIC
    src
)

# Random math operations library
add_library(random_math_operations STATIC
    src/random_math_operations.c
)
target_include_directories(random_math_operations PUBLIC
    src
)

# Test executables
add_executable(test_math_operations
    tests/test_math_operations.c
)
target_link_libraries(test_math_operations
    unity
    math_operations
)

add_executable(test_random_math_operations
    tests/test_random_math_operations.c
)
target_link_libraries(test_random_math_operations
    unity
    random_math_operations
    math_operations
)

# Enable testing and register tests
enable_testing()
add_test(NAME test_math_operations COMMAND test_math_operations)
add_test(NAME test_random_math_operations COMMAND test_random_math_operations)
