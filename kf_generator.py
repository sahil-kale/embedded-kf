import json
import argparse

import os
import shutil

from generator.ingestor import KalmanFilterConfig
from generator.file_content_generator import KalmanFilterConfigGenerator


import os
import shutil


def copy_directory(input_dir, output_dir):
    # Raise an exception if the input directory does not exist
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")

    # Copy the contents of the input directory to the output directory
    # Overwrite the files if they already exist
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
    # add an argument parser for input file
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input file to be processed")

    parser.add_argument(
        "--output_dir",
        help="The output directory for the generated files",
        default="kf_output",
    )

    args = parser.parse_args()

    directory_paths = {
        "output_dir": args.output_dir,
        "inc": f"{args.output_dir}/inc",
        "src": f"{args.output_dir}/src",
    }

    for path in directory_paths.values():
        if not os.path.exists(path):
            os.makedirs(path)

    # open the input file
    with open(args.input_file) as f:
        configs = json.load(f)

        for config in configs:
            kf_config = KalmanFilterConfig(config)
            generator = KalmanFilterConfigGenerator(kf_config)
            c_file_name = f'{kf_config.raw_config["name"]}_config.c'
            h_file_name = f'{kf_config.raw_config["name"]}_config.h'

            # create a file path with the output directory and file name
            c_file_path = f"{directory_paths['src']}/{c_file_name}"
            h_file_path = f"{directory_paths['inc']}/{h_file_name}"

            generator.write_to_file(c_file_path, h_file_path)

        inc_directories_to_copy = [
            "filter/inc",
            "libs/kalman-matrix-utils/inc",
        ]

        src_directories_to_copy = [
            "filter/src",
            "libs/kalman-matrix-utils/src",
        ]

        info_directories_to_copy = [
            "info",
        ]

        for directory in inc_directories_to_copy:
            # convert to absolute path
            directory = os.path.abspath(directory)
            copy_directory(directory, directory_paths["inc"])

        for directory in src_directories_to_copy:
            # convert to absolute path
            directory = os.path.abspath(directory)
            copy_directory(directory, directory_paths["src"])

        for directory in info_directories_to_copy:
            # convert to absolute path
            directory = os.path.abspath(directory)
            copy_directory(directory, directory_paths["output_dir"])


if __name__ == "__main__":
    main()
