#include "configs.hpp"

extern "C" {
#include "kalman.h"
#include "matrix.h"
}

static matrix_data_t X_init_data[2] = {3, 4};
static matrix_data_t F_data[4] = {1, 0.001, 0, 1};
static matrix_data_t P_init_data[4] = {9999, 9999, 9999, 9999};
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

static matrix_data_t temp_H_storage[2] = {0, 0};
static matrix_data_t temp_R_storage[1] = {0};

static matrix_data_t temp_x_hat_storage[2] = {0, 0};
static matrix_data_t S_matrix_storage[1] = {0};
static matrix_data_t K_matrix_storage[2] = {0, 0};

static matrix_data_t temp_measurement_storage_data[1] = {0};
static matrix_data_t Y_matrix_storage[1] = {0};

static matrix_data_t P_Ht_storage[2] = {0, 0};
static matrix_data_t S_inv_storage_data[1] = {0};

static matrix_data_t K_H_storage_data[4] = {0, 0, 0, 0};
static matrix_data_t K_H_P_storage_data[4] = {0, 0, 0, 0};

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
    .temp_Bu_storage = {0, NULL},

    .temp_measurement_storage = {1, temp_measurement_storage_data},

    .H_temp_storage = {2, temp_H_storage},
    .R_temp_storage = {1, temp_R_storage},

    .P_Ht_storage = {2, P_Ht_storage},
    .Y_matrix_storage = {1, Y_matrix_storage},
    .S_matrix_storage = {1, S_matrix_storage},
    .S_inv_matrix_storage = {1, S_inv_storage_data},
    .K_matrix_storage = {2, K_matrix_storage},

    .K_H_storage = {4, K_H_storage_data},
    .K_H_P_storage = {4, K_H_P_storage_data},
};