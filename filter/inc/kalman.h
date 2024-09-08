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
    KF_ERROR_NOT_INITIALIZED,
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

    kf_matrix_storage_S X_matrix_storage;  // min size is num_states * 1
    kf_matrix_storage_S P_matrix_storage;  // min size is num_states * num_states

    kf_matrix_storage_S temp_x_hat_storage;  // min size is num_states * 1
    kf_matrix_storage_S temp_B_storage;      // min size is num_states * num_controls
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

/**
 * @brief Predict the next state of the Kalman filter
 *
 * @param kf_data The Kalman filter data
 * @param u The control input
 *
 * @return kf_error_E Error code indicating the success of the prediction
 *
 * @note Often, in a kalman filter, the prediction step should be run at a fixed time interval to avoid issues with the time
 * update. This library does not explicitly handle time, so the user must ensure that the prediction step is run at a fixed time
 * interval.
 * @warning The kf_data structure must be initialized before calling this function. For optimization purposes, this function does
 * not check null pointers or incorrectly configured matrices to avoid high runtime complexity and computational overhead.
 */
kf_error_E kf_predict(kf_data_S* const kf_data, const matrix_t* const u);

#endif