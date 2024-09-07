#include "kalman.h"

#include <string.h>

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
        invalid_matrix_pointer =
            (config->F == NULL) || (config->P_init == NULL) || (config->Q == NULL) || (config->H == NULL) || (config->R == NULL);
    }

    if ((ret == KF_ERROR_NONE) && invalid_matrix_pointer) {
        ret = KF_ERROR_INVALID_POINTER;
    }

    // F should be square
    if (ret == KF_ERROR_NONE) {
        const matrix_t* F = config->F;
        if (F->rows != F->cols) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }

        kf_data->num_states = F->rows;
    }

    // P_init should be square and have the same dimensions as F
    if (ret == KF_ERROR_NONE) {
        const matrix_t* P_init = config->P_init;
        if ((P_init->rows != P_init->cols) || (P_init->rows != kf_data->num_states)) {
            ret = KF_ERROR_INVALID_DIMENSIONS;
        }
    }

    // Q should be square and have the same dimensions as F
    if (ret == KF_ERROR_NONE) {
        const matrix_t* Q = config->Q;
        if ((Q->rows != Q->cols) || (Q->rows != kf_data->num_states)) {
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
        if ((R->rows != R->cols) || (R->rows != kf_data->num_measurements)) {
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

    // TODO: Give "Storage spaces" to the data via the config struct (just give the pointers to the data)
    // this will allow the user to allocate the memory for the matrices and for us to do the nitty gritty

    // init X, P,

    // init temporary matrices

    if (ret == KF_ERROR_NONE) {
        kf_data->initialized = true;
    }

    return ret;
}