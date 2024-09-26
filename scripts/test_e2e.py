import os
import sys


def run_command(command):
    retcode = os.system(command)
    if retcode != 0:
        raise RuntimeError(f"Command failed with return code {retcode}: {command}")


def main():
    OUTPUT_DIR = "kf_output"

    # Remove the kf_output directory if it exists
    if os.path.exists(OUTPUT_DIR):
        run_command(f"rm -rf {OUTPUT_DIR}")

    sample_input_file = "generator/tests/samples/imu_filter.json"

    # Generate files using kf_generator.py, check for errors
    command = f"python3 kf_generator.py {sample_input_file}"
    run_command(command)

    # Now, change directory to kf_output
    os.chdir(OUTPUT_DIR)

    # Check if the necessary directories are generated
    if not os.path.exists("inc"):
        raise FileNotFoundError("Directory 'inc' not found in the output.")
    if not os.path.exists("src"):
        raise FileNotFoundError("Directory 'src' not found in the output.")

    # Run `bash build_library.sh` and check for errors
    run_command("bash build_library.sh")

    # Check if the build was successful (assuming it creates a 'build' directory)
    if not os.path.exists("build"):
        raise FileNotFoundError("Build directory not found. Build might have failed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
