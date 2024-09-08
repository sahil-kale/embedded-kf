#include "matrix_test_util.hpp"

#include "CppUTest/TestHarness.h"

void verify_matrix_equal(const matrix_t* a, const matrix_t* b) {
    CHECK_EQUAL(a->rows, b->rows);
    CHECK_EQUAL(a->cols, b->cols);

    for (int i = 0; i < a->rows * a->cols; i++) {
        DOUBLES_EQUAL(a->data[i], b->data[i], 0.0001);
    }
}