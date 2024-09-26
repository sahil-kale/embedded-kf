import json
import argparse
import os
import shutil
import sys

from generator.ingestor import KalmanFilterConfig
from generator.file_content_generator import KalmanFilterConfigGenerator


def get_repo_root():
    """Finds the repository root (assuming the script is located within the repo)."""
    # Assumes the script is called from within the repo, typically near the root
    return os.path.abspath(os.path.dirname(__file__))


def copy_directory(input_dir, output_dir):
    """Copy the contents of the input directory to the output directory, with overwrite."""
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        relative_path = os.path.relpath(root, input_dir)
        output_root = os.path.join(output_dir, relative_path)

        if not os.path.exists(output_root):
            os.makedirs(output_root)

        for file in files:
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_root, file)
            shutil.copy2(input_file_path, output_file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input JSON file to be processed")
    parser.add_argument(
        "--output_dir",
        help="The output directory for the generated files",
        default="kf_output",
    )

    args = parser.parse_args()

    repo_root = get_repo_root()  # Get the repository root

    # Check out submodules
    ret_code = os.system("git submodule update --init --recursive")
    if ret_code != 0:
        raise RuntimeError(
            "Failed to update submodules. Ensure the repository is initialized correctly."
        )

    directory_paths = {
        "output_dir": os.path.abspath(args.output_dir),
        "inc": os.path.join(os.path.abspath(args.output_dir), "inc"),
        "src": os.path.join(os.path.abspath(args.output_dir), "src"),
    }

    for path in directory_paths.values():
        if not os.path.exists(path):
            os.makedirs(path)

    # Open the input file and process the JSON configs
    try:
        with open(args.input_file) as f:
            configs = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{args.input_file}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Input file '{args.input_file}' contains invalid JSON.")

    for config in configs:
        kf_config = KalmanFilterConfig(config)
        generator = KalmanFilterConfigGenerator(kf_config)
        c_file_name = f'{kf_config.raw_config["name"]}_config.c'
        h_file_name = f'{kf_config.raw_config["name"]}_config.h'

        c_file_path = os.path.join(directory_paths["src"], c_file_name)
        h_file_path = os.path.join(directory_paths["inc"], h_file_name)

        generator.write_to_file(c_file_path, h_file_path)

    # Prepare directories to copy from, resolving relative paths based on repo root
    inc_directories_to_copy = [
        os.path.join(repo_root, "filter/inc"),
        os.path.join(repo_root, "libs/kalman-matrix-utils/inc"),
    ]

    src_directories_to_copy = [
        os.path.join(repo_root, "filter/src"),
        os.path.join(repo_root, "libs/kalman-matrix-utils/src"),
    ]

    info_directories_to_copy = [
        os.path.join(repo_root, "info"),
    ]

    # Copy include directories
    for directory in inc_directories_to_copy:
        if os.path.exists(directory):
            copy_directory(directory, directory_paths["inc"])
        else:
            raise FileNotFoundError(f"Include directory '{directory}' does not exist.")

    # Copy source directories
    for directory in src_directories_to_copy:
        if os.path.exists(directory):
            copy_directory(directory, directory_paths["src"])
        else:
            raise FileNotFoundError(f"Source directory '{directory}' does not exist.")

    # Copy info directories
    for directory in info_directories_to_copy:
        if os.path.exists(directory):
            copy_directory(directory, directory_paths["output_dir"])
        else:
            raise FileNotFoundError(f"Info directory '{directory}' does not exist.")


if __name__ == "__main__":
    main()
