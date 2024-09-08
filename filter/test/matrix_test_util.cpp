#include "matrix_test_util.hpp"

#include "CppUTest/TestHarness.h"

void verify_matrix_equal(const matrix_t* a, const matrix_t* b) {
    CHECK_EQUAL(a->rows, b->rows);
    CHECK_EQUAL(a->cols, b->cols);

    for (int i = 0; i < a->rows * a->cols; i++) {
        // if not equal, print the index and the values
        if (a->data[i] != b->data[i]) {
            printf("index: %d, a: %f, b: %f\n", i, a->data[i], b->data[i]);
        }
        DOUBLES_EQUAL(a->data[i], b->data[i], 0.0001);
    }
}