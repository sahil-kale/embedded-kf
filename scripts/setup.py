import os
import subprocess
import argparse


def run_command(command):
    """Run a system command and handle errors if any."""
    try:
        result = subprocess.run(command, shell=True, check=True)
        if result.returncode != 0:
            print(f"Command failed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        exit(1)


def update_and_upgrade(skip_upgrade=False):
    """Update and optionally upgrade the system's package list."""
    print("Updating apt package list...")
    run_command("sudo apt-get update")
    if not skip_upgrade:
        print("Upgrading apt packages...")
        run_command("sudo apt-get upgrade -y")
    else:
        print("Skipping apt upgrade...")


def install_apt_components(components):
    """Install components using apt-get."""
    print("Installing apt components...")
    component_list = " ".join(components)
    run_command(f"sudo apt-get install -y {component_list}")


def install_pip_components(components):
    """Install components using pip."""
    print("Installing pip components...")
    component_list = " ".join(components)
    run_command(f"pip3 install {component_list}")


def update_submodules():
    """Update git submodules."""
    print("Updating git submodules...")
    run_command("git submodule update --init --recursive")


if __name__ == "__main__":
    # Argument parser to handle skip_upgrade option
    parser = argparse.ArgumentParser(description="Install necessary development tools.")
    parser.add_argument(
        "--skip-upgrade",
        action="store_true",
        help="Skip the apt upgrade step",
    )
    args = parser.parse_args()

    # Components to install via apt and pip
    apt_components = [
        "git",
        "clang-format",
        "clang-tidy",
        "build-essential",
        "gdb",
        "doxygen",
        "cmake",
        "cpputest",
    ]

    pip_components = ["black"]

    # Execute functions
    update_and_upgrade(skip_upgrade=args.skip_upgrade)
    install_apt_components(apt_components)
    install_pip_components(pip_components)
    update_submodules()
