#include "kalman.h"

#include <string.h>

static bool is_matrix_square_and_matches_states(const matrix_t* matrix, size_t num_states);
static kf_error_E validate_matrix_storage(const kf_matrix_storage_S* storage, size_t required_size);

static bool is_matrix_square_and_matches_states(const matrix_t* matrix, size_t num_states) {
    return (matrix->rows == matrix->cols) && (matrix->rows == num_states);
}

static kf_error_E validate_matrix_storage(const kf_matrix_storage_S* storage, size_t required_size) {
    kf_error_E ret = KF_ERROR_NONE;
    if (storage->data == NULL) {
        ret = KF_ERROR_INVALID_POINTER;
    } else if (storage->size < required_size) {
        ret = KF_ERROR_STORAGE_TOO_SMALL;
    } else {
        ret = KF_ERROR_NONE;
    }
    return ret;
}

kf_error_E kf_init(kf_data_S* const kf_data, const kf_config_S* const config) {
    kf_error_E ret = KF_ERROR_NONE;

    const bool invalid_pointer = (kf_data == NULL) || (config == NULL);

    if (invalid_pointer) {
        ret = KF_ERROR_INVALID_POINTER;
    } else {
        memset(kf_data, 0, sizeof(kf_data_S));
        kf_data->config = config;
    }

    // Make sure all the pointers in the config are not NULL
    bool invalid_matrix_pointer = false;
    if (config != NULL) {
        invalid_matrix_pointer = (config->X_init == NULL) || (config->F == NULL) || (config->P_init == NULL) ||
                                 (config->Q == NULL) || (config->H == NULL) || (config->R == NULL);
    }

    if ((ret == KF_ERROR_NONE) && invalid_matrix_pointer) {
        ret = KF_ERROR_INVALID_POINTER;
    }

    if (ret == KF_ERROR_NONE) {
        kf_data->num_states = config->X_init->rows;
    }

    // F should be square
    if (ret == KF_ERROR_NONE) {
        const matrix_t* F = config->F;
        if (is_matrix_square_and_matches_states(F, kf_data->num_states) == false) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }
    }

    if (ret == KF_ERROR_NONE) {
        const matrix_t* P_init = config->P_init;
        if (is_matrix_square_and_matches_states(P_init, kf_data->num_states) == false) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }
    }

    if (ret == KF_ERROR_NONE) {
        const matrix_t* Q = config->Q;
        if (is_matrix_square_and_matches_states(Q, kf_data->num_states) == false) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }
    }

    // H should have the same number of columns as F
    if (ret == KF_ERROR_NONE) {
        const matrix_t* H = config->H;
        if (H->cols != kf_data->num_states) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }

        kf_data->num_measurements = H->rows;
    }

    // R should be square and should be measurement * measurement
    if (ret == KF_ERROR_NONE) {
        const matrix_t* R = config->R;
        if (is_matrix_square_and_matches_states(R, kf_data->num_measurements) == false) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }
    }

    // if B is defined, then make sure it has the same number of rows as F
    if ((ret == KF_ERROR_NONE) && (config->B != NULL)) {
        const matrix_t* B = config->B;
        if ((B != NULL) && (B->rows != kf_data->num_states)) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }

        kf_data->num_controls = config->B->cols;
    }

    if (ret == KF_ERROR_NONE) {
        ret = validate_matrix_storage(&config->X_matrix_storage, kf_data->num_states);
    }

    if (ret == KF_ERROR_NONE) {
        kf_data->X.rows = kf_data->num_states;
        kf_data->X.cols = 1;
        kf_data->X.data = config->X_matrix_storage.data;  // init temporary matrices

        memcpy(kf_data->X.data, config->X_init->data, kf_data->num_states * sizeof(matrix_data_t));
    }

    if (ret == KF_ERROR_NONE) {
        ret = validate_matrix_storage(&config->P_matrix_storage, kf_data->num_states * kf_data->num_states);
    }

    if (ret == KF_ERROR_NONE) {
        kf_data->P.rows = kf_data->num_states;
        kf_data->P.cols = kf_data->num_states;
        kf_data->P.data = config->P_matrix_storage.data;
        memcpy(kf_data->P.data, config->P_init->data, kf_data->num_states * kf_data->num_states * sizeof(matrix_data_t));
    }

    // init temporary matrices
    if (ret == KF_ERROR_NONE) {
        ret = validate_matrix_storage(&config->temp_x_hat_storage, kf_data->num_states);
    }

    if ((ret == KF_ERROR_NONE) && (kf_data->num_controls > 0)) {
        ret = validate_matrix_storage(&config->temp_B_storage, kf_data->num_states * kf_data->num_controls);
    }

    if (ret == KF_ERROR_NONE) {
        kf_data->initialized = true;
    }

    return ret;
}

kf_error_E kf_predict(kf_data_S* const kf_data, const matrix_t* const u) {
    (void)u;
    kf_error_E ret = KF_ERROR_NONE;

    if (kf_data == NULL) {
        ret = KF_ERROR_INVALID_POINTER;
    } else if (kf_data->initialized == false) {
        ret = KF_ERROR_NOT_INITIALIZED;
    } else {
        ret = KF_ERROR_NONE;
    }

    if (ret == KF_ERROR_NONE) {
        // Calculate the next x hat, x(k|k-1) = F*x(k-1) + B*u
        matrix_mult(kf_data->config->F, &kf_data->X, &kf_data->X, kf_data->config->temp_x_hat_storage.data);

        if (kf_data->num_controls > 0) {
            matrix_t Bu = {kf_data->num_states, 1, kf_data->config->temp_B_storage.data};
            matrix_mult(kf_data->config->B, u, &Bu, kf_data->config->temp_x_hat_storage.data);
            matrix_add_inplace(&kf_data->X, &Bu);
        }

        // Calculate the next P, P(k|k-1) = F*P(k-1)*F' + Q
        matrix_mult(kf_data->config->F, &kf_data->P, &kf_data->P, kf_data->config->temp_x_hat_storage.data);
        matrix_mult_transb(&kf_data->P, kf_data->config->F, &kf_data->P);
        matrix_add_inplace(&kf_data->P, kf_data->config->Q);
    }

    return ret;
}