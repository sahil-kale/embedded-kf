from util import *
import subprocess
import sys
import argparse

EXCLUDE_DIRS = [".vscode", "build", "libs"]
EMBEDDED_EXTENSIONS = (".c", ".h", ".cpp", ".hpp")
PYTHON_EXTENSION = ".py"


def embedded_fmt(dry_run=False):
    """
    Format all C/C++ files at once using clang-format.
    If dry_run is True, it will only check if any formatting is required without making changes.
    """
    embedded_files = get_files_with_extensions(EMBEDDED_EXTENSIONS, EXCLUDE_DIRS)
    if embedded_files:
        if dry_run:
            result = subprocess.run(
                ["clang-format", "--dry-run", "--Werror", *embedded_files],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print("C/C++ files need formatting!")
                sys.exit(1)
        else:
            subprocess.run(["clang-format", "-i", *embedded_files])


def python_fmt(dry_run=False):
    """
    Format all Python files at once using black.
    If dry_run is True, it will only check if any formatting is required without making changes.
    """
    python_files = get_files_with_extensions((PYTHON_EXTENSION,), EXCLUDE_DIRS)
    if python_files:
        if dry_run:
            result = subprocess.run(
                ["black", "--check", *python_files], capture_output=True, text=True
            )
            if result.returncode != 0:
                print("Python formatter failed!")
                sys.exit(1)
        else:
            subprocess.run(["black", *python_files])


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Format source files with specified tools."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check for needed formatting without applying changes.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the formatting with or without dry-run
    embedded_fmt(dry_run=args.dry_run)
    python_fmt(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
