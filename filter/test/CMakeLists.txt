cmake_minimum_required(VERSION 3.14)

set(This kalman_tests)

set(BINARY ${CMAKE_PROJECT_NAME})

project(${This} C CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_C_STANDARD 99)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Og -g -Werror -Wextra -Wall -pedantic -pedantic-errors -Wfloat-equal -Wredundant-decls  -Wswitch-default  -pedantic -Wconversion")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Og -g -Werror -Wextra -Wall")

add_definitions(-DUNIT_TEST)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../inc)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../libs/kalman-matrix-utils/inc)
# add the sources in ../src
file(GLOB_RECURSE KALMAN_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/../src/*.c)

add_library(MAIN_SOURCES_LIB ${KALMAN_SOURCES})
target_compile_options(MAIN_SOURCES_LIB PRIVATE -pedantic -pedantic-errors -Wfloat-equal -Wredundant-decls  -Wswitch-default  -pedantic -Wconversion)

# add the sources in ../../libs/kalman-matrix-utils 
file(GLOB_RECURSE MATRIX_UTILS_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/../../libs/kalman-matrix-utils/src/*.c)

add_library(MATRIX_UTILS_LIB ${MATRIX_UTILS_SOURCES})
target_compile_options(MATRIX_UTILS_LIB PRIVATE -Wno-error -Wno-pedantic)


# Define CPPUTEST_HOME
set(CPPUTEST_HOME /usr)
message(STATUS "Using CppUTest home: ${CPPUTEST_HOME}")
set(CPPUTEST_INCLUDE_DIRS ${CPPUTEST_HOME}/include)
set(CPPUTEST_LIBRARIES ${CPPUTEST_HOME}/lib)
set(CPPUTEST_LDFLAGS CppUTest CppUTestExt)

include_directories(${CPPUTEST_INCLUDE_DIRS})
link_directories(${CPPUTEST_LIBRARIES})

# get all the test sources
file(GLOB TEST_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)

add_executable(${This} ${TEST_SOURCES})
target_link_libraries(${This} ${CPPUTEST_LDFLAGS} MAIN_SOURCES_LIB MATRIX_UTILS_LIB)