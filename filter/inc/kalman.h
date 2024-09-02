#ifndef KALMAN_H
#define KALMAN_H
#include <stdbool.h>
#include <stddef.h>

#include "matrix.h"

typedef enum { KF_ERROR_NONE = 0, KF_ERROR_INVALID_POINTER, KF_ERROR_COUNT } kf_error_E;

typedef struct {
    const matrix_t const *F, B;
    const matrix_t const *Q, P_init;
    const matrix_t const *H, R;
} kf_config_S;

typedef struct {
    kf_config_S* config;

    bool initialized;
} kf_data_S;

kf_error_E kf_init(kf_data_S* const kf_data);

#endif