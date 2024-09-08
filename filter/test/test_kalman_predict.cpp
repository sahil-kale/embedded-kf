#include "CppUTest/TestHarness.h"

extern "C" {
#include "kalman.h"
#include "matrix.h"
}

#include "matrix_test_util.hpp"

static matrix_data_t X_init_data[2] = {3, 4};
static matrix_data_t F_data[4] = {1, 0.001, 0, 1};
static matrix_data_t P_init_data[4] = {0, 0, 0, 0};
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

static matrix_data_t temp_x_hat_storage[2] = {0, 0};

static matrix_data_t temp_S_storage[1] = {0};
static matrix_data_t temp_K_storage[2] = {0, 0};

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

    .temp_x_hat_storage = {2, temp_x_hat_storage},
    .temp_B_storage = {0, NULL},

    .temp_S_storage = {1, temp_S_storage},
    .temp_K_storage = {2, temp_K_storage},
};

TEST_GROUP(kalman_predict_test){void setup(){} void teardown(){}};

TEST(kalman_predict_test, kalman_predict_not_initialized) {
    kf_error_E error = kf_predict(NULL, NULL);
    CHECK_EQUAL(KF_ERROR_INVALID_POINTER, error);

    kf_data_S kf_data;
    memset(&kf_data, 0, sizeof(kf_data));
    error = kf_predict(&kf_data, NULL);
    CHECK_EQUAL(KF_ERROR_NOT_INITIALIZED, error);
}

TEST(kalman_predict_test, kalman_predict_simple) {
    kf_data_S kf_data;
    kf_error_E error = kf_init(&kf_data, &default_simple_config);
    // 2 is num states

    matrix_data_t aux_data[2] = {0, 0};

    // Calculate the next x hat, x(k|k-1) = F*x(k-1)
    matrix_data_t X_storage_test[2] = {0, 0};
    matrix_t x_hat = {2, 1, X_storage_test};
    matrix_mult(&F, &kf_data.X, &x_hat, aux_data);

    // Calculate the next P, P(k|k-1) = F*P(k-1)*F' + Q
    matrix_data_t P_storage_test[4] = {0, 0, 0, 0};
    matrix_t P = {2, 2, P_storage_test};

    matrix_mult(&F, &kf_data.P, &P, aux_data);
    matrix_mult_transb(&P, &F, &P);
    matrix_add_inplace(&P, &Q);

    error = kf_predict(&kf_data, NULL);

    CHECK_EQUAL(KF_ERROR_NONE, error);

    verify_matrix_equal(&x_hat, &kf_data.X);
    verify_matrix_equal(&P, &kf_data.P);
}

TEST(kalman_predict_test, kalman_predict_simple_with_control_input) {
    kf_data_S kf_data;
    kf_config_S config_with_B = default_simple_config;
    static matrix_data_t B_data[4] = {1, 1, 1, 1};
    static matrix_t B = {2, 2, B_data};
    config_with_B.B = &B;
    static matrix_data_t temp_B_storage[4] = {0, 0, 0, 0};
    config_with_B.temp_B_storage = {4, temp_B_storage};

    kf_error_E error = kf_init(&kf_data, &config_with_B);
    CHECK_EQUAL(KF_ERROR_NONE, error);
    // 2 is num states, but using 4 for B vector aux
    matrix_data_t aux_data[4] = {0, 0};

    matrix_data_t u_data[2] = {1, 1};
    matrix_t u = {2, 1, u_data};

    // Calculate the next x hat, x(k|k-1) = F*x(k-1) + B*u
    matrix_data_t X_storage_test[2] = {0, 0};
    matrix_t x_hat = {2, 1, X_storage_test};
    matrix_mult(&F, &kf_data.X, &x_hat, aux_data);

    // temporary matrix to store B*u
    matrix_data_t Bu_storage[2] = {0, 0};
    matrix_t Bu = {2, 1, Bu_storage};
    matrix_mult(&B, &u, &Bu, aux_data);
    matrix_add_inplace(&x_hat, &Bu);

    // Calculate the next P, P(k|k-1) = F*P(k-1)*F' + Q
    matrix_data_t P_storage_test[4] = {0, 0, 0, 0};
    matrix_t P = {2, 2, P_storage_test};

    matrix_mult(&F, &kf_data.P, &P, aux_data);
    matrix_mult_transb(&P, &F, &P);
    matrix_add_inplace(&P, &Q);

    error = kf_predict(&kf_data, &u);
    CHECK_EQUAL(KF_ERROR_NONE, error);

    verify_matrix_equal(&x_hat, &kf_data.X);
    verify_matrix_equal(&P, &kf_data.P);
}

TEST(kalman_predict_test, invalid_control_input_dims) {
    kf_data_S kf_data;
    kf_config_S config_with_B = default_simple_config;
    static matrix_data_t B_data[4] = {1, 1, 1, 1};
    static matrix_t B = {2, 2, B_data};
    config_with_B.B = &B;
    static matrix_data_t temp_B_storage[4] = {0, 0, 0, 0};
    config_with_B.temp_B_storage = {4, temp_B_storage};
    kf_error_E error = kf_init(&kf_data, &config_with_B);
    CHECK_EQUAL(KF_ERROR_NONE, error);

    matrix_data_t u_data[3] = {1, 1, 1};
    matrix_t u = {3, 1, u_data};

    error = kf_predict(&kf_data, &u);
    CHECK_EQUAL(KF_ERROR_INVALID_DIMENSIONS, error);

    // Give a correct U matrix, but make B matrix NULL. Expect an error because B matrix is NULL
    kf_config_S config_with_null_B = default_simple_config;
    config_with_null_B.B = NULL;
    error = kf_init(&kf_data, &config_with_null_B);
    CHECK_EQUAL(KF_ERROR_NONE, error);

    error = kf_predict(&kf_data, &u);
    CHECK_EQUAL(KF_ERROR_CONTROL_MATRIX_NOT_ENABLED, error);
}