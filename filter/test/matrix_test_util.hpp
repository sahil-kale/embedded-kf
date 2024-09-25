#ifndef MATRIX_TEST_UTIL_HPP
#define MATRIX_TEST_UTIL_HPP

extern "C" {
#include "matrix_types.h"
}

void verify_matrix_equal(const matrix_t* a, const matrix_t* b);

#endif