cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(KalmanFilterLibrary VERSION 1.0 LANGUAGES C)

# Set C standard to C99
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED True)

# Add compiler flags for all warnings, errors, and pedantic mode
add_compile_options(-Wall -Wextra -pedantic -Werror)

# Define source and include directories
set(SRC_DIR src)
set(INC_DIR inc)

# Use globbing to automatically find all .c and .h files in src and inc directories
file(GLOB SOURCES "${SRC_DIR}/*.c")
file(GLOB HEADERS "${INC_DIR}/*.h")

# Add include directories
include_directories(${INC_DIR})

# Create the shared library
add_library(kalman_filter SHARED ${SOURCES} ${HEADERS})

# Add versioning information to the shared library
set_target_properties(kalman_filter PROPERTIES VERSION ${PROJECT_VERSION})

# If this is part of a larger CMake project, we allow this CMake file to be called
if(NOT TARGET kalman_filter)
    add_library(KalmanFilter::kalman_filter ALIAS kalman_filter)
endif()
