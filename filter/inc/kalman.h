#ifndef KALMAN_H
#define KALMAN_H
#include <stdbool.h>
#include <stddef.h>

#include "matrix.h"

typedef enum {
    KF_ERROR_NONE = 0,
    KF_ERROR_INVALID_POINTER,
    KF_ERROR_INVALID_DIMENSIONS,
    KF_ERROR_COUNT
} kf_error_E;

typedef struct {
    const matrix_t* F;
    const matrix_t* B;

    const matrix_t* Q;
    const matrix_t* P_init;

    const matrix_t* H;
    const matrix_t* R;
} kf_config_S;

typedef struct {
    kf_config_S const* config;

    bool initialized;

    size_t num_states;
    size_t num_measurements;

    size_t num_controls;
} kf_data_S;

kf_error_E kf_init(kf_data_S* const kf_data, const kf_config_S* const config);

#endif