#ifndef KALMAN_H
#define KALMAN_H
#include <stdbool.h>
#include <stddef.h>

#include "matrix_types.h"

/**
 * @brief Error codes for the Kalman filter functions.
 */
typedef enum {
    KF_ERROR_NONE = 0,                   /**< No error */
    KF_ERROR_INVALID_POINTER,            /**< Invalid pointer */
    KF_ERROR_INVALID_DIMENSIONS,         /**< Invalid matrix dimensions */
    KF_ERROR_STORAGE_TOO_SMALL,          /**< Insufficient storage allocated */
    KF_ERROR_NOT_INITIALIZED,            /**< Kalman filter not initialized */
    KF_ERROR_CONTROL_MATRIX_NOT_ENABLED, /**< Control matrix not enabled */
    KF_ERROR_COUNT                       /**< Total number of error types */
} kf_error_E;

/**
 * @brief Structure for storing matrix data.
 */
typedef struct {
    size_t size;         /**< Size of the matrix storage */
    matrix_data_t* data; /**< Pointer to the matrix data */
} kf_matrix_storage_S;

/**
 * @brief Kalman filter configuration structure.
 *
 * This structure contains all the necessary matrices and storage required to initialize
 * and operate a Kalman filter.
 */
typedef struct {
    const matrix_t* X_init; /**< Initial state estimate matrix */
    const matrix_t* F;      /**< State transition matrix */
    const matrix_t* B;      /**< Control input matrix (optional) */

    const matrix_t* Q;      /**< Process noise covariance matrix */
    const matrix_t* P_init; /**< Initial state covariance matrix */

    const matrix_t* H; /**< State to measurement transformation matrix */
    const matrix_t* R; /**< Measurement noise covariance matrix */

    kf_matrix_storage_S X_matrix_storage; /**< Storage for the state estimate matrix, size: num_states * 1 */
    kf_matrix_storage_S P_matrix_storage; /**< Storage for the covariance matrix, size: num_states * num_states */

    kf_matrix_storage_S temp_X_hat_matrix_storage; /**< Temporary storage for the state estimate, size: num_states * 1 */
    kf_matrix_storage_S temp_Bu_matrix_storage;    /**< Temporary storage for control matrix, size: num_states * 1 */

    kf_matrix_storage_S temp_Z_matrix_storage; /**< Temporary storage for measurement vector, size: num_measurements * 1 */

    kf_matrix_storage_S
        H_temp_storage; /**< Temporary storage for the transformation matrix, size: num_measurements * num_states */
    kf_matrix_storage_S R_temp_storage; /**< Temporary storage for the measurement noise covariance matrix, size: num_measurements
                                         * num_measurements */

    kf_matrix_storage_S P_Ht_storage;     /**< Storage for P * H^T, size: num_states * num_measurements */
    kf_matrix_storage_S Y_matrix_storage; /**< Storage for innovation vector (residual), size: num_measurements * 1 */
    kf_matrix_storage_S
        S_matrix_storage; /**< Storage for innovation covariance matrix, size: num_measurements * num_measurements */
    kf_matrix_storage_S S_inv_matrix_storage; /**< Storage for the inverse of S, size: num_measurements * num_measurements */

    kf_matrix_storage_S K_matrix_storage; /**< Storage for Kalman gain matrix, size: num_states * num_measurements */

    kf_matrix_storage_S K_H_storage;   /**< Storage for K * H, size: num_states * num_states */
    kf_matrix_storage_S K_H_P_storage; /**< Storage for K * H * P, size: num_states * num_states */
} kf_config_S;

/**
 * @brief Kalman filter data structure.
 *
 * This structure stores the current state and covariance of the Kalman filter,
 * along with temporary matrices used during predictions and updates.
 */
typedef struct {
    kf_config_S const* config; /**< Configuration for the Kalman filter */

    bool initialized; /**< Flag indicating whether the filter has been initialized */

    matrix_t X; /**< Current state estimate matrix */
    matrix_t P; /**< Current covariance matrix */

    matrix_t H_temp; /**< Temporary matrix for H during prediction step, used for asynchronous updates */
    matrix_t R_temp; /**< Temporary matrix for R during prediction step */

    matrix_t P_Ht_temp;  /**< Temporary matrix for P * H^T during the update step */
    matrix_t Y_temp;     /**< Temporary matrix for the innovation vector (residual) */
    matrix_t S_temp;     /**< Temporary matrix for the innovation covariance matrix */
    matrix_t S_inv_temp; /**< Temporary matrix for the inverse of S */
    matrix_t K_temp;     /**< Temporary matrix for the Kalman gain */

    matrix_t K_H_temp;   /**< Temporary matrix for K * H */
    matrix_t K_H_P_temp; /**< Temporary matrix for K * H * P */

    size_t num_states;       /**< Number of states in the system */
    size_t num_measurements; /**< Number of measurements in the system */
    size_t num_controls;     /**< Number of control inputs in the system */
} kf_data_S;

/**
 * @brief Initialize the Kalman filter.
 *
 * This function initializes the Kalman filter by setting up its configuration
 * and preparing the necessary matrices.
 *
 * @param kf_data The Kalman filter data structure
 * @param config The configuration for the Kalman filter, must be statically allocated
 *
 * @return kf_error_E Error code indicating the success of the initialization
 */
kf_error_E kf_init(kf_data_S* const kf_data, const kf_config_S* const config);

/**
 * @brief Predict the next state of the Kalman filter.
 *
 * This function performs the prediction step of the Kalman filter using the state transition
 * matrix and the optional control input matrix.
 *
 * @param kf_data The Kalman filter data
 * @param u The control input (can be NULL if no control input is provided)
 *
 * @return kf_error_E Error code indicating the success of the prediction
 *
 * @note The prediction step should be run at a fixed time interval to avoid time update issues.
 * This library does not explicitly handle time, so the user must ensure the prediction step
 * is run at a fixed interval.
 * @warning The kf_data structure must be initialized before calling this function. Null pointer
 * checks and incorrect configurations are not performed for optimization purposes.
 */
kf_error_E kf_predict(kf_data_S* const kf_data, const matrix_t* const u);

/**
 * @brief Update the Kalman filter with a new measurement.
 *
 * This function performs the update step of the Kalman filter using the provided measurement vector.
 *
 * @param kf_data The Kalman filter data
 * @param z The measurement vector
 * @param measurement_validity Array of boolean values indicating the validity of each measurement.
 * Can be NULL if all measurements are valid. Assumed to be of size num_measurements (rows in the Z matrix).
 * @param num_measurements The number of measurements in the measurement vector. This is ignored if
 * measurement_validity is NULL.
 *
 * @return kf_error_E Error code indicating the success of the update
 */
kf_error_E kf_update(kf_data_S* const kf_data, const matrix_t* const z, const bool* const measurement_validity,
                     const size_t num_measurements);

#endif
