#ifndef KALMAN_H
#define KALMAN_H
#include <stdbool.h>
#include <stddef.h>

#include "matrix.h"

typedef enum {
    KF_ERROR_NONE = 0,
    KF_ERROR_INVALID_POINTER,
    KF_ERROR_INVALID_DIMENSIONS,
    KF_ERROR_STORAGE_TOO_SMALL,
    KF_ERROR_COUNT
} kf_error_E;

typedef struct {
    size_t size;
    matrix_data_t* data;
} kf_matrix_storage_S;

typedef struct {
    const matrix_t* X_init;
    const matrix_t* F;
    const matrix_t* B;

    const matrix_t* Q;
    const matrix_t* P_init;

    const matrix_t* H;
    const matrix_t* R;

    kf_matrix_storage_S X_matrix_storage;
    kf_matrix_storage_S P_matrix_storage;
} kf_config_S;

typedef struct {
    kf_config_S const* config;

    bool initialized;

    matrix_t X;
    matrix_t P;

    size_t num_states;
    size_t num_measurements;
    size_t num_controls;
} kf_data_S;

/**
 * @brief Initialize the Kalman filter
 *
 * @param kf_data The Kalman filter data structure
 * @param config The configuration for the Kalman filter, must be statically allocated
 *
 * @return kf_error_E Error code indicating the success of the initialization
 */
kf_error_E kf_init(kf_data_S* const kf_data, const kf_config_S* const config);

#endif