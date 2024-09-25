import os


def get_files_with_extensions(extensions, exclude_dirs, base_path="."):
    """
    Get a list of all files with the specified extensions, excluding certain directories.
    """
    files = []
    for root, dirs, filenames in os.walk(base_path):
        # Modify 'dirs' in-place to exclude unwanted directories by name
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files.extend(
            os.path.join(root, filename)
            for filename in filenames
            if filename.endswith(extensions)
        )
    return files


def build_from_cmake(cmake_path, build_dir, cmake_args):
    """
    Run cmake and build the project.
    """
    os.system(f"mkdir -p {build_dir}")
    os.chdir(build_dir)
    cmd = f"{cmake_path} .. {' '.join(cmake_args)}"
    os.system(cmd)
    ret = os.system("make all")
    if ret != 0:
        print("Error building the application")
        exit(1)
