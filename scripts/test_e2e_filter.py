import os
import argparse

from util import build_from_cmake


def main():
    # use ctypesgen to generate the python bindings
    # output to generator/e2e_evaluator/e2e_simulator_bindings.py
    # and generate from header files in filter/inc and libs/kalman-matrix-utils/inc

    command = "ctypesgen -o generator/e2e_evaluator/e2e_simulator_bindings.py filter/inc/kalman.h libs/kalman-matrix-utils/inc/matrix_types.h -I libs/kalman-matrix-utils/inc"
    os.system(command)


    os.chdir("generator/e2e_evaluator")
    build_from_cmake("cmake", "build", ["-DCMAKE_BUILD_TYPE=Debug"])

if __name__ == "__main__":
    main()
