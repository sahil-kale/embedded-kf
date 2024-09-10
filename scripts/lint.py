import os
from util import *

INCLUDE_DIRS = [
    "filter/inc",
    "libs/kalman-matrix-utils/inc",
]

# Add additional strict checks for clang-tidy
STRICT_CHECKS = [
    "clang-analyzer-*",  # Static analysis checks
    "cppcoreguidelines-*",  # C++ Core Guidelines
    "modernize-*",  # Modernize to newer C++ standards (if applicable)
    "performance-*",  # Performance optimizations
    "readability-*",  # Readability improvements
    "bugprone-*",  # Bug-prone code patterns
    "portability-*",  # Portability checks for different platforms
    "misc-*",  # Miscellaneous checks
    "hicpp-*",  # High-integrity C++ checks
    "concurrency-*",  # Concurrency-related issues
]

# Define checks to be excluded
EXCLUDED_CHECKS = [
    "readability-identifier-length",  # Exclude identifier length check
    "clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling",
]

# Build include directories string for the clang-tidy command
INCLUDE_DIR_STR = " -I" + " -I".join(INCLUDE_DIRS)


def run_clang_tidy(file, checks, include_dir_str):
    cmd = (
        f"clang-tidy {file} -checks={checks} -warnings-as-errors=* -- {include_dir_str}"
    )

    print(f"Running: {cmd}")
    result = os.system(cmd)
    if result != 0:
        raise RuntimeError(f"clang-tidy failed on {file}")


def main():
    # Find all of the .c files inside filter/src
    c_files = get_files_with_extensions((".c"), ["build", "test"], base_path="filter")

    # Convert the list of strict checks and exclusions to a comma-separated string
    checks = ",".join(STRICT_CHECKS + [f"-{check}" for check in EXCLUDED_CHECKS])

    # Run clang-tidy on all of the files with the most pedantic options
    for c_file in c_files:
        try:
            run_clang_tidy(c_file, checks, INCLUDE_DIR_STR)
        except RuntimeError as e:
            print(e)
            exit(1)  # Exit with error code if clang-tidy fails


if __name__ == "__main__":
    main()
