#include "CppUTest/TestHarness.h"

extern "C" {
#include "kalman.h"
#include "matrix.h"
}

static matrix_data_t X_init_data[2] = {3, 4};
static matrix_data_t F_data[4] = {1, 0.001, 0, 1};
static matrix_data_t P_init_data[4] = {1, 0, 0, 1};
static matrix_data_t Q_data[4] = {1, 0, 0, 1};

static matrix_data_t R_data[1] = {1};
static matrix_data_t H_data[2] = {1, 0};

static matrix_t X_init = {2, 1, X_init_data};
static matrix_t F = {2, 2, F_data};
static matrix_t P_init = {2, 2, P_init_data};
static matrix_t Q = {2, 2, Q_data};
static matrix_t R = {1, 1, R_data};
static matrix_t H = {1, 2, H_data};

static matrix_data_t X_storage[2] = {0, 0};
static matrix_data_t P_storage[4] = {1, 0, 0, 1};

const kf_config_S default_simple_config = {
    .X_init = &X_init,
    .F = &F,
    .B = NULL,
    .Q = &Q,
    .P_init = &P_init,
    .H = &H,
    .R = &R,

    .X_matrix_storage = {2, X_storage},
    .P_matrix_storage = {4, P_storage},
};

TEST_GROUP(kalman_api_test){void setup(){} void teardown(){}};

// Test that the kalman filter initialization fails when the pointer is NULL
TEST(kalman_api_test, kalman_init_null_pointer) {
    kf_error_E error = kf_init(NULL, NULL);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);

    kf_data_S kf_data;
    memset(&kf_data, 0, sizeof(kf_data));
    error = kf_init(&kf_data, NULL);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);

    error = kf_init(NULL, &default_simple_config);
}

// Test filter invalid matrix dimension between F and P_init
TEST(kalman_api_test, simple_kalman_init) {
    kf_data_S kf_data;

    kf_error_E error = kf_init(&kf_data, &default_simple_config);

    CHECK_EQUAL(KF_ERROR_NONE, error);
    CHECK_EQUAL(true, kf_data.initialized);

    // check the config pointers are equal
    CHECK_EQUAL(&default_simple_config, kf_data.config);

    CHECK_EQUAL(2, kf_data.num_states);
    CHECK_EQUAL(1, kf_data.num_measurements);
}

// Test that the kalman filter initialization fails when the X_init matrix is NULL
TEST(kalman_api_test, kalman_init_null_X_init) {
    kf_data_S kf_data;
    kf_config_S config_with_null_X_init = default_simple_config;
    config_with_null_X_init.X_init = NULL;

    kf_error_E error = kf_init(&kf_data, &config_with_null_X_init);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);
}

// Test that the F matrix is square
TEST(kalman_api_test, invalid_F_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_F_dims = default_simple_config;
    static matrix_t F_bad = {1, 2, F_data};
    config_with_invalid_F_dims.F = &F_bad;

    kf_error_E error = kf_init(&kf_data, &config_with_invalid_F_dims);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // Try with a NULL F matrix
    kf_config_S config_with_null_F = default_simple_config;
    config_with_null_F.F = NULL;

    error = kf_init(&kf_data, &config_with_null_F);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // test 3x3 F matrix, should fail with invalid dimensions
    kf_config_S config_with_3x3_F = default_simple_config;
    static matrix_data_t F_3x3_data[9] = {1, 0, 0, 0, 1, 0, 0, 0, 1};
    static matrix_t F_3x3 = {3, 3, F_3x3_data};
    config_with_3x3_F.F = &F_3x3;

    error = kf_init(&kf_data, &config_with_3x3_F);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);
    CHECK_EQUAL(false, kf_data.initialized);
}

// Test invalid matrix dimensions
TEST(kalman_api_test, invalid_P_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_P_dims = default_simple_config;
    static matrix_t P_init_bad = {2, 1, P_init_data};
    config_with_invalid_P_dims.P_init = &P_init_bad;

    kf_error_E error = kf_init(&kf_data, &config_with_invalid_P_dims);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // Try with a NULL P matrix
    kf_config_S config_with_null_P = default_simple_config;
    config_with_null_P.P_init = NULL;

    error = kf_init(&kf_data, &config_with_null_P);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);
}

// Test invalid matrix dimensions for Q
TEST(kalman_api_test, invalid_Q_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_Q_dims = default_simple_config;
    static matrix_t Q_bad = {1, 2, Q_data};
    config_with_invalid_Q_dims.Q = &Q_bad;

    kf_error_E error = kf_init(&kf_data, &config_with_invalid_Q_dims);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // Try with a NULL Q matrix
    kf_config_S config_with_null_Q = default_simple_config;
    config_with_null_Q.Q = NULL;

    error = kf_init(&kf_data, &config_with_null_Q);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);
}

// Test invalid matrix dimensions for H
TEST(kalman_api_test, invalid_H_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_H_dims = default_simple_config;
    static matrix_t H_bad = {2, 1, H_data};
    config_with_invalid_H_dims.H = &H_bad;

    kf_error_E error = kf_init(&kf_data, &config_with_invalid_H_dims);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // Try with a NULL H matrix
    kf_config_S config_with_null_H = default_simple_config;
    config_with_null_H.H = NULL;

    error = kf_init(&kf_data, &config_with_null_H);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);
}

// Test invalid matrix dimensions for R
TEST(kalman_api_test, invalid_R_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_R_dims = default_simple_config;
    static matrix_t R_bad = {1, 2, R_data};
    config_with_invalid_R_dims.R = &R_bad;

    kf_error_E error = kf_init(&kf_data, &config_with_invalid_R_dims);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // Try with a NULL R matrix
    kf_config_S config_with_null_R = default_simple_config;
    config_with_null_R.R = NULL;

    error = kf_init(&kf_data, &config_with_null_R);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);
}

// Test B matrix dimensions with control
TEST(kalman_api_test, invalid_B_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_B_dims = default_simple_config;
    static matrix_t B_bad = {1, 2, F_data};
    config_with_invalid_B_dims.B = &B_bad;

    kf_error_E error = kf_init(&kf_data, &config_with_invalid_B_dims);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // test with correct B matrix, verify num_controls is set
    kf_config_S config_with_B = default_simple_config;
    static matrix_t B = {2, 3, F_data};
    config_with_B.B = &B;

    error = kf_init(&kf_data, &config_with_B);
    CHECK_EQUAL(KF_ERROR_NONE, error);
    CHECK_EQUAL(true, kf_data.initialized);
    CHECK_EQUAL(3, kf_data.num_controls);
}

// Test storage space for X
TEST(kalman_api_test, storage_space_X) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    kf_error_E error = kf_init(&kf_data, &config_with_storage);
    CHECK_EQUAL(KF_ERROR_NONE, error);
    CHECK_EQUAL(true, kf_data.initialized);
    CHECK_EQUAL(config_with_storage.X_matrix_storage.data, kf_data.X.data);

    // Check that the X matrix data is identical to the X init data
    for (size_t i = 0; i < X_init.rows; i++) {
        CHECK_EQUAL(X_init_data[i], matrix_get(&kf_data.X, i, 0));
    }

    // Test invalid pointer for X matrix storage
    kf_config_S config_with_null_X_storage = default_simple_config;
    config_with_null_X_storage.X_matrix_storage.data = NULL;

    error = kf_init(&kf_data, &config_with_null_X_storage);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // Test invalid size for X matrix storage
    kf_config_S config_with_invalid_X_storage = default_simple_config;
    config_with_invalid_X_storage.X_matrix_storage.size = 1;

    error = kf_init(&kf_data, &config_with_invalid_X_storage);
    CHECK_EQUAL(KF_ERROR_STORAGE_TOO_SMALL, error);
    CHECK_EQUAL(false, kf_data.initialized);
}

// Test storage space for P
TEST(kalman_api_test, storage_space_P) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    kf_error_E error = kf_init(&kf_data, &config_with_storage);
    CHECK_EQUAL(KF_ERROR_NONE, error);
    CHECK_EQUAL(true, kf_data.initialized);
    CHECK_EQUAL(config_with_storage.P_matrix_storage.data, kf_data.P.data);

    // Check that the P matrix data is identical to the P init data
    for (size_t i = 0; i < P_init.rows; i++) {
        for (size_t j = 0; j < P_init.cols; j++) {
            CHECK_EQUAL(P_init_data[i * P_init.cols + j], matrix_get(&kf_data.P, i, j));
        }
    }

    // Test invalid pointer for P matrix storage
    kf_config_S config_with_null_P_storage = default_simple_config;
    config_with_null_P_storage.P_matrix_storage.data = NULL;

    error = kf_init(&kf_data, &config_with_null_P_storage);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
    CHECK_EQUAL(false, kf_data.initialized);

    // Test invalid size for P matrix storage
    kf_config_S config_with_invalid_P_storage = default_simple_config;
    config_with_invalid_P_storage.P_matrix_storage.size = 1;

    error = kf_init(&kf_data, &config_with_invalid_P_storage);
    CHECK_EQUAL(KF_ERROR_STORAGE_TOO_SMALL, error);
    CHECK_EQUAL(false, kf_data.initialized);
}