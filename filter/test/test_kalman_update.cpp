#include "CppUTest/TestHarness.h"

extern "C" {
#include "cholesky.h"
#include "kalman.h"
#include "matrix.h"
}

#include "configs.hpp"
#include "matrix_test_util.hpp"

TEST_GROUP(kalman_update_test){void setup(){} void teardown(){}};

TEST(kalman_update_test, kalman_update_not_initialized) {
    kf_error_E error = kf_update(NULL, NULL, NULL, 0U);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);

    kf_data_S kf_data;
    memset(&kf_data, 0, sizeof(kf_data));

    matrix_data_t z_data[1] = {0};
    matrix_t z = {1, 1, z_data};

    error = kf_update(&kf_data, &z, NULL, 0U);
    CHECK_EQUAL(KF_ERROR_NOT_INITIALIZED, error);
}

TEST(kalman_update_test, kalman_update_invalid_Z) {
    kf_data_S kf_data;
    kf_error_E error = kf_init(&kf_data, &default_simple_config);
    CHECK_EQUAL(KF_ERROR_NONE, error);

    error = kf_update(&kf_data, NULL, NULL, 0U);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);
}

TEST(kalman_update_test, kalman_update_simple) {
    kf_data_S kf_data;
    kf_error_E error = kf_init(&kf_data, &default_simple_config);
    CHECK_EQUAL(KF_ERROR_NONE, error);

    matrix_data_t Z_data[1] = {0};
    matrix_t Z = {1, 1, Z_data};
    matrix_data_t aux_data[4] = {0, 0};

    matrix_data_t y_data[1] = {0};
    matrix_t Y = {1, 1, y_data};

    matrix_data_t P_data[4];
    memcpy(P_data, default_simple_config.P_init->data, 4 * sizeof(matrix_data_t));
    matrix_t P = {2, 2, P_data};

    matrix_data_t x_hat_data[2];
    memcpy(x_hat_data, kf_data.X.data, 2 * sizeof(matrix_data_t));
    matrix_t x_hat = {2, 1, x_hat_data};

    // calculate innovation: z - H * x_hat
    matrix_data_t H_x_hat_data[1] = {0};
    matrix_t H_x_hat = {1, 1, H_x_hat_data};

    matrix_mult(default_simple_config.H, &x_hat, &H_x_hat, aux_data);

    matrix_sub(&Z, &H_x_hat, &Y);

    // calculate S: H * P * H^T + R
    matrix_data_t H_P_data[2] = {0, 0};
    matrix_t H_P = {1, 2, H_P_data};

    matrix_mult(default_simple_config.H, &P, &H_P, aux_data);

    matrix_data_t H_P_Ht_data[1] = {0};
    matrix_t H_P_Ht = {1, 1, H_P_Ht_data};

    matrix_mult_transb(&H_P, default_simple_config.H, &H_P_Ht);

    matrix_data_t S_data[1] = {0};
    matrix_t S = {1, 1, S_data};

    // copy R to S
    matrix_copy(kf_data.config->R, &S);

    matrix_add_inplace(&S, &H_P_Ht);

    // calculate K: P * H^T * S^-1
    matrix_data_t K_data[2] = {0, 0};
    matrix_t K = {2, 1, K_data};

    matrix_data_t S_inv_data[1] = {1};
    matrix_t S_inv = {1, 1, S_inv_data};

    cholesky_decompose_lower(&S);
    matrix_invert_lower(&S, &S_inv);

    matrix_data_t P_Ht_data[2] = {0, 0};
    matrix_t P_Ht = {2, 1, P_Ht_data};

    matrix_mult_transb(&P, default_simple_config.H, &P_Ht);

    matrix_mult(&P_Ht, &S_inv, &K, aux_data);

    // calculate x_hat_new: x_hat + K * Y
    matrix_data_t x_hat_new_data[2] = {0, 0};
    matrix_t x_hat_new = {2, 1, x_hat_new_data};

    matrix_mult(&K, &Y, &x_hat_new, aux_data);
    matrix_add_inplace(&x_hat, &x_hat_new);

    // calculate P_new = (I - K * H) * P
    // which is equivalent to P - K * H * P
    matrix_data_t K_H_data[4] = {0, 0, 0, 0};
    matrix_t K_H = {2, 2, K_H_data};

    matrix_mult(&K, default_simple_config.H, &K_H, aux_data);

    matrix_data_t K_H_P_data[4] = {0, 0, 0, 0};

    matrix_t K_H_P = {2, 2, K_H_P_data};
    matrix_mult(&K_H, &P, &K_H_P, aux_data);

    matrix_sub(&P, &K_H_P, &P);

    error = kf_update(&kf_data, &Z, NULL, 0U);
    CHECK_EQUAL(KF_ERROR_NONE, error);

    verify_matrix_equal(&x_hat, &kf_data.X);
    verify_matrix_equal(&P, &kf_data.P);
}

// Test an update with a measurement that is invalid (async measurement)