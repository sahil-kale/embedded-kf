#ifndef KALMAN_H
#define KALMAN_H
#include <stdbool.h>
#include <stddef.h>

typedef enum {
    KF_ERROR_NONE = 0,
    KF_ERROR_INVALID_POINTER,
    KF_ERROR_COUNT
} kf_error_E;

typedef struct {
    bool initialized;
} kf_data_S;

kf_error_E kf_init(kf_data_S * const kf_data);

#endif