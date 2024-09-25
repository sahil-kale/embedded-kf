import os
import argparse

TESTS_EXE_NAME = "kalman_tests"

from util import build_from_cmake


def main(debug):
    os.chdir("filter/test")
    build_from_cmake("cmake", "build", ["-DCMAKE_BUILD_TYPE=Debug"])

    if debug:
        os.system(f"gdb ./{TESTS_EXE_NAME}")
    else:
        os.system(f"./{TESTS_EXE_NAME}")


if __name__ == "__main__":
    # create an arg parser for whether to debug or not
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Debug mode", action="store_true")
    args = parser.parse_args()

    main(args.debug)
