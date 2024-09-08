import os
import subprocess

EXCLUDE_DIRS = [".vscode", "build", "libs"]
EMBEDDED_EXTENSIONS = (".c", ".h", ".cpp", ".hpp")
PYTHON_EXTENSION = ".py"


def get_files_with_extensions(extensions):
    """
    Get a list of all files with the specified extensions, excluding certain directories.
    """
    files = []
    for root, dirs, filenames in os.walk("."):
        # Modify 'dirs' in-place to exclude unwanted directories by name
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        files.extend(
            os.path.join(root, filename)
            for filename in filenames
            if filename.endswith(extensions)
        )
    return files


def format_files(command, files):
    """
    Run the specified format command on a list of files.
    """
    if files:
        subprocess.run([command, *files])


def embedded_fmt():
    """
    Format C/C++ files using clang-format.
    """
    embedded_files = get_files_with_extensions(EMBEDDED_EXTENSIONS)
    for file in embedded_files:
        subprocess.run(["clang-format", "-i", file])


def python_fmt():
    """
    Format Python files using black.
    """
    python_files = get_files_with_extensions((PYTHON_EXTENSION,))
    format_files("black", python_files)


if __name__ == "__main__":
    embedded_fmt()
    python_fmt()
