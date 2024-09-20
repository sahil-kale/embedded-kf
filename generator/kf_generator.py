import json
import argparse

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)


from ingestor import KalmanFilterConfig
from c_file_generator import KalmanFilterConfigGenerator


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

    # if directory does not exist, create it
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # open the input file
    with open(args.input_file) as f:
        configs = json.load(f)

        for config in configs:
            kf_config = KalmanFilterConfig(config)
            generator = KalmanFilterConfigGenerator(kf_config)
            file_name = f'{kf_config.raw_config["name"]}_config.c'

            # create a file path with the output directory and file name
            file_path = f"{args.output_dir}/{file_name}"

            generator.write_to_file(file_path)


if __name__ == "__main__":
    main()
