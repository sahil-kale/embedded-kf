#include "CppUTest/TestHarness.h"

extern "C" {
#include "kalman.h"
}

TEST_GROUP(kalman_api_test){void setup(){} void teardown(){}};

// Test that the kalman filter initialization fails when the pointer is NULL
TEST(kalman_api_test, kalman_init_null_pointer) {
    kf_error_E error = kf_init(NULL);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);

    kf_data_S kf_data;
    memset(&kf_data, 0, sizeof(kf_data));
    error = kf_init(&kf_data);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);
}