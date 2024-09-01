#include "kalman.h"

kf_error_E kf_init(kf_data_S * const kf_data) {
    kf_error_E ret = KF_ERROR_NONE;
    
    if (kf_data == NULL) {
        ret = KF_ERROR_INVALID_POINTER;
    }
    return ret;
}