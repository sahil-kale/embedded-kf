import os

EXCLUDE_DIRS = [".vscode", "build", "libs"]


def embedded_fmt():
    # get all .c, .h, .cpp, and .hpp files in the project. Ignore the excluded directories and recursively ignore or search for files
    files = []
    for root, dirs, filenames in os.walk("."):
        dirs[:] = [
            d
            for d in dirs
            if os.path.join(root, d) not in [os.path.join(".", e) for e in EXCLUDE_DIRS]
        ]
        for filename in filenames:
            if filename.endswith((".c", ".h", ".cpp", ".hpp")):
                files.append(os.path.join(root, filename))

    # format all the files
    for file in files:
        os.system(f"clang-format -i {file}")


def python_fmt():
    # get all .py files in the project. Ignore the excluded directories and recursively ignore or search for files
    files = []
    for root, dirs, filenames in os.walk("."):
        dirs[:] = [
            d
            for d in dirs
            if os.path.join(root, d) not in [os.path.join(".", e) for e in EXCLUDE_DIRS]
        ]
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.join(root, filename))

    # format all the files
    file_arg = " ".join(files)
    os.system(f"black {file_arg}")


if __name__ == "__main__":
    embedded_fmt()
    python_fmt()
