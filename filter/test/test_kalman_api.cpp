#include "CppUTest/TestHarness.h"

extern "C" {
#include "kalman.h"
}

TEST_GROUP(kalman_api_test) {
    void setup() {}
    void teardown() {}
};

// Test that the kalman filter initialization fails when the pointer is NULL
TEST(kalman_api_test, kalman_init_null_pointer) {
    kf_error_E error = kf_init(NULL);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
}