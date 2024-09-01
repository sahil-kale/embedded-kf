import os

# update apt
os.system("sudo apt-get update")
# upgrade apt
os.system("sudo apt-get upgrade -y")

# components to install via apt
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

# components to install via pip
pip_components = ["black"]

# install apt components
components = " ".join(apt_components)
os.system(f"sudo apt-get install -y {components}")

# install pip components
components = " ".join(pip_components)
os.system(f"pip3 install {components}")

# update submodules
os.system("git submodule update --init --recursive")
