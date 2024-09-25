cmake_minimum_required(VERSION 3.14)

set(This e2e_kalman_tests)

set(BINARY ${CMAKE_PROJECT_NAME})

project(${This} C CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_C_STANDARD 99)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Og -g -Werror -Wextra -Wall -pedantic -pedantic-errors -Wfloat-equal -Wredundant-decls  -Wswitch-default -pedantic -Wconversion")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Og -g -Werror -Wextra -Wall")

# Directories for sources
set(FILTER_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../filter)
set(MATRIX_UTILS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../libs/kalman-matrix-utils)

include_directories(${FILTER_DIR}/inc)
include_directories(${MATRIX_UTILS_DIR}/inc)

# Collect the sources for Kalman filter
file(GLOB_RECURSE KALMAN_SOURCES ${FILTER_DIR}/src/*.c)

# Output source directories
set(KF_OUTPUT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../kf_output)
include_directories(${KF_OUTPUT_DIR}/inc)
file(GLOB_RECURSE KF_OUTPUT_SOURCES ${KF_OUTPUT_DIR}/src/*.c)

# Collect the sources for the matrix utilities
file(GLOB_RECURSE MATRIX_UTILS_SOURCES ${MATRIX_UTILS_DIR}/src/*.c)

# Create a single shared library combining all sources
add_library(KALMAN_SO_LIB SHARED ${KALMAN_SOURCES} ${KF_OUTPUT_SOURCES} ${MATRIX_UTILS_SOURCES})
target_compile_options(KALMAN_SO_LIB PRIVATE -pedantic -pedantic-errors -Wfloat-equal -Wredundant-decls -Wswitch-default -pedantic -Wconversion)

# Output to .so file
set_target_properties(KALMAN_SO_LIB PROPERTIES OUTPUT_NAME "kalman_combined" SUFFIX ".so")
