cmake_minimum_required(VERSION 3.14)
project(corn-test-cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(GTest REQUIRED)

add_executable(corn_tests
    src/math_operations.cpp
    src/random_math_operations.cpp
    tests/math_operations_test.cpp
    tests/random_math_operations_test.cpp
)

target_include_directories(corn_tests PRIVATE ${CMAKE_SOURCE_DIR}/src)
target_link_libraries(corn_tests GTest::gtest_main)

enable_testing()
include(GoogleTest)
gtest_discover_tests(corn_tests)
