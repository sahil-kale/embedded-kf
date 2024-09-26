#ifndef KALMAN_H
#define KALMAN_H
#include <stdbool.h>
#include <stddef.h>

#include "matrix_types.h"

typedef enum {
    KF_ERROR_NONE = 0,
    KF_ERROR_INVALID_POINTER,
    KF_ERROR_INVALID_DIMENSIONS,
    KF_ERROR_STORAGE_TOO_SMALL,
    KF_ERROR_NOT_INITIALIZED,
    KF_ERROR_CONTROL_MATRIX_NOT_ENABLED,
    KF_ERROR_COUNT
} kf_error_E;

typedef struct {
    size_t size;
    matrix_data_t* data;
} kf_matrix_storage_S;

typedef struct {
    const matrix_t* X_init;  // initial state estimate
    const matrix_t* F;       // state transition matrix
    const matrix_t* B;       // control input matrix (optional)

    const matrix_t* Q;       // process noise covariance matrix
    const matrix_t* P_init;  // initial state covariance matrix

    const matrix_t* H;  // state to measurement transformation matrix
    const matrix_t* R;  // measurement noise covariance matrix

    kf_matrix_storage_S X_matrix_storage;  // min size is num_states * 1
    kf_matrix_storage_S P_matrix_storage;  // min size is num_states * num_states

    kf_matrix_storage_S temp_X_hat_matrix_storage;  // min size is num_states * 1
    kf_matrix_storage_S temp_Bu_matrix_storage;     // min size is num_states * 1

    kf_matrix_storage_S temp_Z_matrix_storage;  // min size is num_measurements * 1

    kf_matrix_storage_S H_temp_storage;  // min size is num_measurements * num_states
    kf_matrix_storage_S
        R_temp_storage;  // min size is num_measurements * num_measurements (todo: figure out if this needs to be reshaped?)

    kf_matrix_storage_S P_Ht_storage;          // min size is num_states * num_measurements
    kf_matrix_storage_S Y_matrix_storage;      // min size is num_measurements * 1
    kf_matrix_storage_S S_matrix_storage;      // min size is num_measurements * num_measurements
    kf_matrix_storage_S S_inv_matrix_storage;  // min size is num_measurements * num_measurements

    kf_matrix_storage_S K_matrix_storage;  // min size is num_states * num_measurements

    kf_matrix_storage_S K_H_storage;    // min size is num_states * num_states
    kf_matrix_storage_S K_H_P_storage;  // min size is num_states * num_states
} kf_config_S;

typedef struct {
    kf_config_S const* config;

    bool initialized;

    matrix_t X;
    matrix_t P;

    matrix_t H_temp;  // used during prediction step; separate matrix required to support asynchronous updates as we modify the H&
                      // R matrix to do so
    matrix_t R_temp;

    matrix_t P_Ht_temp;
    matrix_t Y_temp;
    matrix_t S_temp;
    matrix_t S_inv_temp;
    matrix_t K_temp;

    matrix_t K_H_temp;
    matrix_t K_H_P_temp;

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

/**
 * @brief Update the Kalman filter with a new measurement
 * @param kf_data The Kalman filter data
 * @param z The measurement vector
 * @param measurement_validity Array of boolean values indicating the validity of each measurement. Can leave NULL if all
 * measurements are valid. Assumed to be of size num_measurements (rows in Z matrix)
 * @param num_measurements The number of measurements in the measurement vector. Unused if measurement_validity is NULL
 *
 * @return kf_error_E Error code indicating the success of the update
 */
kf_error_E kf_update(kf_data_S* const kf_data, const matrix_t* const z, const bool* const measurement_validity,
                     const size_t num_measurements);

#endif