import os
import argparse

TESTS_EXE_NAME = "kalman_tests"

def main(debug):

    # chdir to "application"
    os.chdir("filter")
    os.chdir("test")

    # make a build directory
    os.system("mkdir -p build")
    os.chdir("build")

    # run "cmake ."
    cmd = r'cmake .. -DCMAKE_BUILD_TYPE=Debug -G "Unix Makefiles"'
    os.system(cmd)
    # make the application, check that the ret code is 0
    ret = os.system("make all")
    if ret != 0:
        print("Error building the application")
        exit(1)

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
