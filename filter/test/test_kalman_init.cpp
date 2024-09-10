#include "CppUTest/TestHarness.h"

extern "C" {
#include "kalman.h"
#include "matrix.h"
}

#include "configs.hpp"
#include "matrix_test_util.hpp"

TEST_GROUP(kalman_api_test){void setup(){} void teardown(){}};

static kf_error_E check_kf_init(kf_data_S* kf_data, const kf_config_S* config, kf_error_E expected_error) {
    kf_error_E error = kf_init(kf_data, config);
    CHECK_EQUAL(expected_error, error);

    if (expected_error == KF_ERROR_NONE) {
        CHECK_EQUAL(config, kf_data->config);
    } else {
        CHECK_EQUAL(false, kf_data->initialized);
    }

    return error;
}

// Test that the kalman filter initialization fails when the pointer is NULL
TEST(kalman_api_test, kalman_init_null_pointer) {
    kf_error_E error = kf_init(NULL, NULL);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);

    kf_data_S kf_data;
    memset(&kf_data, 0, sizeof(kf_data));
    check_kf_init(&kf_data, NULL, KF_ERROR_INVALID_POINTER);

    error = kf_init(NULL, &default_simple_config);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
}

// Test filter invalid matrix dimension between F and P_init
TEST(kalman_api_test, simple_kalman_init) {
    kf_data_S kf_data;

    check_kf_init(&kf_data, &default_simple_config, KF_ERROR_NONE);

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

    check_kf_init(&kf_data, &config_with_null_X_init, KF_ERROR_INVALID_POINTER);
}

// Test that the F matrix is square
TEST(kalman_api_test, invalid_F_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_F_dims = default_simple_config;
    matrix_data_t F_data[3] = {1, 0, 0};
    static matrix_t F_bad = {1, 2, F_data};
    config_with_invalid_F_dims.F = &F_bad;

    check_kf_init(&kf_data, &config_with_invalid_F_dims, KF_ERROR_INVALID_DIMENSIONS);

    // Try with a NULL F matrix
    kf_config_S config_with_null_F = default_simple_config;
    config_with_null_F.F = NULL;

    check_kf_init(&kf_data, &config_with_null_F, KF_ERROR_INVALID_POINTER);

    // test 3x3 F matrix, should fail with invalid dimensions
    kf_config_S config_with_3x3_F = default_simple_config;
    static matrix_data_t F_3x3_data[9] = {1, 0, 0, 0, 1, 0, 0, 0, 1};
    static matrix_t F_3x3 = {3, 3, F_3x3_data};
    config_with_3x3_F.F = &F_3x3;

    check_kf_init(&kf_data, &config_with_3x3_F, KF_ERROR_INVALID_DIMENSIONS);
}

// Test invalid matrix dimensions
TEST(kalman_api_test, invalid_P_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_P_dims = default_simple_config;
    matrix_data_t P_init_data[3] = {1, 0, 0};
    static matrix_t P_init_bad = {2, 1, P_init_data};
    config_with_invalid_P_dims.P_init = &P_init_bad;

    check_kf_init(&kf_data, &config_with_invalid_P_dims, KF_ERROR_INVALID_DIMENSIONS);

    // Try with a NULL P matrix
    kf_config_S config_with_null_P = default_simple_config;
    config_with_null_P.P_init = NULL;

    check_kf_init(&kf_data, &config_with_null_P, KF_ERROR_INVALID_POINTER);
}

// Test invalid matrix dimensions for Q
TEST(kalman_api_test, invalid_Q_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_Q_dims = default_simple_config;
    matrix_data_t Q_data[3] = {1, 0, 0};
    static matrix_t Q_bad = {1, 2, Q_data};
    config_with_invalid_Q_dims.Q = &Q_bad;

    check_kf_init(&kf_data, &config_with_invalid_Q_dims, KF_ERROR_INVALID_DIMENSIONS);

    // Try with a NULL Q matrix
    kf_config_S config_with_null_Q = default_simple_config;
    config_with_null_Q.Q = NULL;

    check_kf_init(&kf_data, &config_with_null_Q, KF_ERROR_INVALID_POINTER);
}

// Test invalid matrix dimensions for H
TEST(kalman_api_test, invalid_H_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_H_dims = default_simple_config;
    matrix_data_t H_data[3] = {1, 0, 0};
    static matrix_t H_bad = {2, 1, H_data};
    config_with_invalid_H_dims.H = &H_bad;

    check_kf_init(&kf_data, &config_with_invalid_H_dims, KF_ERROR_INVALID_DIMENSIONS);

    // Try with a NULL H matrix
    kf_config_S config_with_null_H = default_simple_config;
    config_with_null_H.H = NULL;

    check_kf_init(&kf_data, &config_with_null_H, KF_ERROR_INVALID_POINTER);
}

// Test invalid matrix dimensions for R
TEST(kalman_api_test, invalid_R_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_R_dims = default_simple_config;
    matrix_data_t R_data[3] = {1, 0, 0};
    static matrix_t R_bad = {1, 2, R_data};
    config_with_invalid_R_dims.R = &R_bad;

    check_kf_init(&kf_data, &config_with_invalid_R_dims, KF_ERROR_INVALID_DIMENSIONS);

    // Try with a NULL R matrix
    kf_config_S config_with_null_R = default_simple_config;
    config_with_null_R.R = NULL;

    check_kf_init(&kf_data, &config_with_null_R, KF_ERROR_INVALID_POINTER);
}

// Test B matrix dimensions with control
TEST(kalman_api_test, invalid_B_matrix_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_invalid_B_dims = default_simple_config;

    matrix_data_t F_data[4] = {1, 0.001, 0, 1};
    static matrix_t B_bad = {1, 2, F_data};
    config_with_invalid_B_dims.B = &B_bad;

    check_kf_init(&kf_data, &config_with_invalid_B_dims, KF_ERROR_INVALID_DIMENSIONS);

    // test with correct B matrix, verify num_controls is set
    kf_config_S config_with_B = default_simple_config;
    static matrix_t B = {2, 3, F_data};
    config_with_B.B = &B;
    static matrix_data_t temp_Bu_storage[2] = {0};
    config_with_B.temp_Bu_storage = {2, temp_Bu_storage};

    check_kf_init(&kf_data, &config_with_B, KF_ERROR_NONE);
    CHECK_EQUAL(3, kf_data.num_controls);

    // Test with NULL B storage matrix
    kf_config_S config_with_null_B_storage = config_with_B;
    config_with_null_B_storage.temp_Bu_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_B_storage, KF_ERROR_INVALID_POINTER);

    // Test with invalid B storage matrix size
    config_with_null_B_storage.temp_Bu_storage.size = 1;
    config_with_null_B_storage.temp_Bu_storage.data = temp_Bu_storage;

    check_kf_init(&kf_data, &config_with_null_B_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

static void test_storage_space_with_matrix_init(kf_data_S* const kf_data, const kf_config_S* config_with_null_matrix,
                                                const kf_config_S* config_with_bad_size,
                                                const matrix_t* const matrix_to_ensure_is_identical,
                                                const matrix_t* const matrix_to_compare) {
    check_kf_init(kf_data, &default_simple_config, KF_ERROR_NONE);

    // Check that the matrix data is identical to the matrix init data
    verify_matrix_equal(matrix_to_ensure_is_identical, matrix_to_compare);

    // Test invalid pointer for matrix storage
    check_kf_init(kf_data, config_with_null_matrix, KF_ERROR_INVALID_POINTER);

    // Test invalid size for matrix storage
    check_kf_init(kf_data, config_with_bad_size, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage space for X
TEST(kalman_api_test, storage_space_X) {
    // Test invalid pointer for X matrix storage
    kf_config_S config_with_null_X_storage = default_simple_config;
    config_with_null_X_storage.X_matrix_storage.data = NULL;

    // Test invalid size for X matrix storage
    kf_config_S config_with_invalid_X_storage = default_simple_config;
    config_with_invalid_X_storage.X_matrix_storage.size = 1;

    kf_data_S kf_data;
    memset(&kf_data, 0, sizeof(kf_data));
    test_storage_space_with_matrix_init(&kf_data, &config_with_null_X_storage, &config_with_invalid_X_storage,
                                        default_simple_config.X_init, &kf_data.X);
}

// Test storage space for P
TEST(kalman_api_test, storage_space_P) {
    kf_data_S kf_data;
    memset(&kf_data, 0, sizeof(kf_data));

    // Test invalid pointer for P matrix storage
    kf_config_S config_with_null_P_storage = default_simple_config;
    config_with_null_P_storage.P_matrix_storage.data = NULL;

    // Test invalid size for P matrix storage
    kf_config_S config_with_invalid_P_storage = default_simple_config;
    config_with_invalid_P_storage.P_matrix_storage.size = 1;

    test_storage_space_with_matrix_init(&kf_data, &config_with_null_P_storage, &config_with_invalid_P_storage,
                                        default_simple_config.P_init, &kf_data.P);
}

// Test storage space for temp_x_hat
TEST(kalman_api_test, storage_space_temp_x_hat) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    // Test invalid pointer for temp_x_hat matrix storage
    kf_config_S config_with_null_temp_x_hat_storage = default_simple_config;
    config_with_null_temp_x_hat_storage.temp_x_hat_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_temp_x_hat_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for temp_x_hat matrix storage
    kf_config_S config_with_invalid_temp_x_hat_storage = default_simple_config;
    config_with_invalid_temp_x_hat_storage.temp_x_hat_storage.size = 1;

    check_kf_init(&kf_data, &config_with_invalid_temp_x_hat_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage space for S_matrix_storage
TEST(kalman_api_test, storage_space_temp_S) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    POINTERS_EQUAL(config_with_storage.S_matrix_storage.data, kf_data.S_temp.data);
    CHECK_EQUAL(1, kf_data.S_temp.rows);
    CHECK_EQUAL(1, kf_data.S_temp.cols);

    // Test invalid pointer for temp_S matrix storage
    kf_config_S config_with_null_S_matrix_storage = default_simple_config;
    config_with_null_S_matrix_storage.S_matrix_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_S_matrix_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for temp_S matrix storage
    kf_config_S config_with_invalid_S_matrix_storage = default_simple_config;
    config_with_invalid_S_matrix_storage.S_matrix_storage.size = 0;

    check_kf_init(&kf_data, &config_with_invalid_S_matrix_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage space for K_matrix_storage
TEST(kalman_api_test, storage_space_temp_K) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    POINTERS_EQUAL(config_with_storage.K_matrix_storage.data, kf_data.K_temp.data);
    CHECK_EQUAL(2, kf_data.K_temp.rows);
    CHECK_EQUAL(1, kf_data.K_temp.cols);

    // Test invalid pointer for temp_K matrix storage
    kf_config_S config_with_null_K_matrix_storage = default_simple_config;
    config_with_null_K_matrix_storage.K_matrix_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_K_matrix_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for temp_K matrix storage
    kf_config_S config_with_invalid_K_matrix_storage = default_simple_config;
    config_with_invalid_K_matrix_storage.K_matrix_storage.size = 1;

    check_kf_init(&kf_data, &config_with_invalid_K_matrix_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage space for temp Y storage
TEST(kalman_api_test, storage_space_temp_Y) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    POINTERS_EQUAL(config_with_storage.Y_matrix_storage.data, kf_data.Y_temp.data);
    CHECK_EQUAL(1, kf_data.Y_temp.rows);
    CHECK_EQUAL(1, kf_data.Y_temp.cols);

    // Test invalid pointer for temp_Y matrix storage
    kf_config_S config_with_null_Y_matrix_storage = default_simple_config;
    config_with_null_Y_matrix_storage.Y_matrix_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_Y_matrix_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for temp_Y matrix storage
    kf_config_S config_with_invalid_Y_matrix_storage = default_simple_config;
    config_with_invalid_Y_matrix_storage.Y_matrix_storage.size = 0;

    check_kf_init(&kf_data, &config_with_invalid_Y_matrix_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage space for temp P*Ht
TEST(kalman_api_test, storage_space_temp_P_Ht) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    POINTERS_EQUAL(config_with_storage.P_Ht_storage.data, kf_data.P_Ht_temp.data);
    CHECK_EQUAL(2, kf_data.P_Ht_temp.rows);
    CHECK_EQUAL(1, kf_data.P_Ht_temp.cols);

    // Test invalid pointer for temp_P_Ht matrix storage
    kf_config_S config_with_null_P_Ht_storage = default_simple_config;
    config_with_null_P_Ht_storage.P_Ht_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_P_Ht_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for temp_P_Ht matrix storage
    kf_config_S config_with_invalid_P_Ht_storage = default_simple_config;
    config_with_invalid_P_Ht_storage.P_Ht_storage.size = 1;

    check_kf_init(&kf_data, &config_with_invalid_P_Ht_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage space for temp_measurement_storage
TEST(kalman_api_test, storage_space_temp_measurement) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    // Test invalid pointer for temp_measurement matrix storage
    kf_config_S config_with_null_temp_measurement_storage = default_simple_config;
    config_with_null_temp_measurement_storage.temp_measurement_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_temp_measurement_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for temp_measurement matrix storage
    kf_config_S config_with_invalid_temp_measurement_storage = default_simple_config;
    config_with_invalid_temp_measurement_storage.temp_measurement_storage.size = 0;

    check_kf_init(&kf_data, &config_with_invalid_temp_measurement_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage for S_inv
TEST(kalman_api_test, storage_space_for_s_inv) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    POINTERS_EQUAL(config_with_storage.S_inv_matrix_storage.data, kf_data.S_inv_temp.data);
    CHECK_EQUAL(1, kf_data.S_inv_temp.rows);
    CHECK_EQUAL(1, kf_data.S_inv_temp.cols);

    // Test invalid pointer for S_inv matrix storage
    kf_config_S config_with_null_S_inv_storage = default_simple_config;
    config_with_null_S_inv_storage.S_inv_matrix_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_S_inv_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for S_inv matrix storage
    kf_config_S config_with_invalid_S_inv_storage = default_simple_config;
    config_with_invalid_S_inv_storage.S_inv_matrix_storage.size = 0;

    check_kf_init(&kf_data, &config_with_invalid_S_inv_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage for K_H
TEST(kalman_api_test, storage_space_for_K_H) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    POINTERS_EQUAL(config_with_storage.K_H_storage.data, kf_data.K_H_temp.data);
    CHECK_EQUAL(2, kf_data.K_H_temp.rows);
    CHECK_EQUAL(2, kf_data.K_H_temp.cols);

    // Test invalid pointer for K_H matrix storage
    kf_config_S config_with_null_K_H_storage = default_simple_config;
    config_with_null_K_H_storage.K_H_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_K_H_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for K_H matrix storage
    kf_config_S config_with_invalid_K_H_storage = default_simple_config;
    config_with_invalid_K_H_storage.K_H_storage.size = 0;

    check_kf_init(&kf_data, &config_with_invalid_K_H_storage, KF_ERROR_STORAGE_TOO_SMALL);
}

// Test storage for K_H_P
TEST(kalman_api_test, storage_space_for_K_H_P) {
    kf_data_S kf_data;
    kf_config_S config_with_storage = default_simple_config;

    check_kf_init(&kf_data, &config_with_storage, KF_ERROR_NONE);

    POINTERS_EQUAL(config_with_storage.K_H_P_storage.data, kf_data.K_H_P_temp.data);
    CHECK_EQUAL(2, kf_data.K_H_P_temp.rows);
    CHECK_EQUAL(2, kf_data.K_H_P_temp.cols);

    // Test invalid pointer for K_H_P matrix storage
    kf_config_S config_with_null_K_H_P_storage = default_simple_config;
    config_with_null_K_H_P_storage.K_H_P_storage.data = NULL;

    check_kf_init(&kf_data, &config_with_null_K_H_P_storage, KF_ERROR_INVALID_POINTER);

    // Test invalid size for K_H_P matrix storage
    kf_config_S config_with_invalid_K_H_P_storage = default_simple_config;
    config_with_invalid_K_H_P_storage.K_H_P_storage.size = 0;

    check_kf_init(&kf_data, &config_with_invalid_K_H_P_storage, KF_ERROR_STORAGE_TOO_SMALL);
}