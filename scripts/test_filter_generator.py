import os
import pytest

if __name__ == "__main__":
    # grab all the python files in generator/tests
    test_files = []
    for root, _, files in os.walk("generator/tests"):
        for file in files:
            if file.endswith(".py"):
                test_files.append(os.path.join(root, file))

    # Run pytest programmatically to enable breakpoints
    pytest_args = test_files  # this passes the test files to pytest
    # Add additional pytest arguments if needed, e.g., "-s" to capture stdout
    pytest_args.append("-s")  # "-s" ensures that print statements and debuggers work

    # Run pytest
    exit_code = pytest.main(pytest_args)

    # Exit with the appropriate code from pytest
    exit(exit_code)
