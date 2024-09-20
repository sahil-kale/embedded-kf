import pytest
import json

# add the package from ../generator to the path
import os
import sys

# Get the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

SIMPLE_CONFIG_PATH = "generator/tests/samples/simple_filter.json"
SIMPLE_CONFIG_PATH_WITH_CONTROL = (
    "generator/tests/samples/simple_filter_with_control.json"
)

from generator.ingestor import *
from generator.c_file_generator import *

SIMPLE_CONFIG_PATH = "generator/tests/samples/simple_filter.json"
SIMPLE_CONFIG_PATH_WITH_CONTROL = (
    "generator/tests/samples/simple_filter_with_control.json"
)


@pytest.mark.parametrize(
    "config_path",
    [SIMPLE_CONFIG_PATH, SIMPLE_CONFIG_PATH_WITH_CONTROL],
)
def test_preprocessor_defines(config_path: str):
    # load the simple config
    with open(config_path) as f:
        config = json.load(f)

        simple_kf_config = config[0]
        simple_kf_config_converted = KalmanFilterConfig(simple_kf_config)

        generated_config = KalmanFilterConfigGenerator(simple_kf_config_converted)

        expected_compiler_defines = [
            "#define SIMPLE_KF_NUM_STATES (2U)",
            "#define SIMPLE_KF_NUM_MEASUREMENTS (1U)",
        ]

        if config_path == SIMPLE_CONFIG_PATH_WITH_CONTROL:
            expected_compiler_defines.append("#define SIMPLE_KF_NUM_CONTROLS (1U)")

        for define in expected_compiler_defines:
            assert define in generated_config.generated_preprocessor_defines


# fmt: off
@pytest.mark.parametrize(
    "config_path, matrix_name, rows_expr, cols_expr",
    [
        (SIMPLE_CONFIG_PATH, "F", "SIMPLE_KF_NUM_STATES", "SIMPLE_KF_NUM_STATES"),
        (SIMPLE_CONFIG_PATH, "H", "SIMPLE_KF_NUM_MEASUREMENTS", "SIMPLE_KF_NUM_STATES"),
        (SIMPLE_CONFIG_PATH, "Q", "SIMPLE_KF_NUM_STATES", "SIMPLE_KF_NUM_STATES"),
        (
            SIMPLE_CONFIG_PATH,
            "R",
            "SIMPLE_KF_NUM_MEASUREMENTS",
            "SIMPLE_KF_NUM_MEASUREMENTS",
        ),
        (
            SIMPLE_CONFIG_PATH_WITH_CONTROL,
            "B",
            "SIMPLE_KF_NUM_STATES",
            "SIMPLE_KF_NUM_CONTROLS",
        ),
        (SIMPLE_CONFIG_PATH, "P_init", "SIMPLE_KF_NUM_STATES", "SIMPLE_KF_NUM_STATES"),
        (SIMPLE_CONFIG_PATH, "X_init", "SIMPLE_KF_NUM_STATES", "(1U)"),
    ],
)
# fmt: on
def test_config_matrix(
    config_path: str, matrix_name: str, rows_expr: str, cols_expr: str
):
    # Load the simple config
    with open(config_path) as f:
        config = json.load(f)

    simple_kf_config = config[0]
    simple_kf_config_converted = KalmanFilterConfig(simple_kf_config)

    generated_config = KalmanFilterConfigGenerator(simple_kf_config_converted)

    # Get the matrix by name (F or H)
    matrix = getattr(generated_config.config, matrix_name).flatten()

    # Flatten the matrix to a string
    matrix_flattened_str = "{" + ", ".join(str(x) for x in matrix) + "}"

    # Build the expected matrix definition output
    matrix_data_name = f"SIMPLE_KF_{matrix_name}_data"
    matrix_name_full = f"SIMPLE_KF_{matrix_name}"

    expected_matrix_output = [
        f"static matrix_data_t {matrix_data_name}[{rows_expr} * {cols_expr}] = {matrix_flattened_str};",
        f"static matrix_t {matrix_name_full} = {{{rows_expr}, {cols_expr}, {matrix_data_name}}};",
    ]

    # Check if the expected output is in generated config definitions
    for line in expected_matrix_output:
        assert line in generated_config.generated_config_definitions


# fmt: off
@pytest.mark.parametrize(
    "config_path, variable_name, rows_expr, cols_expr",
    [
        (SIMPLE_CONFIG_PATH, "X_matrix_storage", "SIMPLE_KF_NUM_STATES", "(1U)"),
        (
            SIMPLE_CONFIG_PATH,
            "P_matrix_storage",
            "SIMPLE_KF_NUM_STATES",
            "SIMPLE_KF_NUM_STATES",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "temp_X_hat_matrix_storage",
            "SIMPLE_KF_NUM_STATES",
            "(1U)",
        ),
        (
            SIMPLE_CONFIG_PATH_WITH_CONTROL,
            "temp_Bu_matrix_storage",
            "SIMPLE_KF_NUM_STATES",
            "(1U)",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "temp_Z_matrix_storage",
            "SIMPLE_KF_NUM_MEASUREMENTS",
            "(1U)",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "H_temp_storage",
            "SIMPLE_KF_NUM_MEASUREMENTS",
            "SIMPLE_KF_NUM_STATES",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "R_temp_storage",
            "SIMPLE_KF_NUM_MEASUREMENTS",
            "SIMPLE_KF_NUM_MEASUREMENTS",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "P_Ht_storage",
            "SIMPLE_KF_NUM_STATES",
            "SIMPLE_KF_NUM_MEASUREMENTS",
        ),
        (SIMPLE_CONFIG_PATH, "Y_matrix_storage", "SIMPLE_KF_NUM_MEASUREMENTS", "(1U)"),
        (
            SIMPLE_CONFIG_PATH,
            "S_matrix_storage",
            "SIMPLE_KF_NUM_MEASUREMENTS",
            "SIMPLE_KF_NUM_MEASUREMENTS",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "S_inv_matrix_storage",
            "SIMPLE_KF_NUM_MEASUREMENTS",
            "SIMPLE_KF_NUM_MEASUREMENTS",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "K_matrix_storage",
            "SIMPLE_KF_NUM_STATES",
            "SIMPLE_KF_NUM_MEASUREMENTS",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "K_H_storage",
            "SIMPLE_KF_NUM_STATES",
            "SIMPLE_KF_NUM_STATES",
        ),
        (
            SIMPLE_CONFIG_PATH,
            "K_H_P_storage",
            "SIMPLE_KF_NUM_STATES",
            "SIMPLE_KF_NUM_STATES",
        ),
    ],
)
# fmt: on
def test_storage_matrix(config_path, variable_name, rows_expr, cols_expr):
    with open(config_path) as f:
        config = json.load(f)

        simple_kf_config = config[0]
        simple_kf_config_converted = KalmanFilterConfig(simple_kf_config)

        generated_config = KalmanFilterConfigGenerator(simple_kf_config_converted)

        expected_matrix_output = [
            f"static matrix_data_t {simple_kf_config['name'].upper()}_{variable_name}[{rows_expr} * {cols_expr}] = {{0}};",
        ]

        # Check if the expected output is in generated config definitions
        for line in expected_matrix_output:
            assert line in generated_config.generated_storage_definitions
