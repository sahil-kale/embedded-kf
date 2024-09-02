#include "kalman.h"

kf_error_E kf_init(kf_data_S* const kf_data) {
    kf_error_E ret = KF_ERROR_NONE;
    const bool invalid_pointer = (kf_data == NULL) || (kf_data->config == NULL);

    if (invalid_pointer) {
        ret = KF_ERROR_INVALID_POINTER;
    }

    // verify dimensions are correct

    // init temporary matrices

    return ret;
}