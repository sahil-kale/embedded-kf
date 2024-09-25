import os
import argparse

from util import build_from_cmake


def main():
    os.chdir("generator/e2e_evaluator")
    build_from_cmake("cmake", "build", ["-DCMAKE_BUILD_TYPE=Debug"])


if __name__ == "__main__":
    main()
