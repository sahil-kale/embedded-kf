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
from generator.file_content_generator import *

SIMPLE_CONFIG_PATH = "generator/tests/samples/simple_filter.json"
SIMPLE_CONFIG_PATH_WITH_CONTROL = (
    "generator/tests/samples/simple_filter_with_control.json"
)


def load_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return KalmanFilterConfig(config[0])


def format_matrix_with_newlines(matrix: np.ndarray, cols_expr: str) -> str:
    rows, cols = matrix.shape
    matrix_rows = []
    for i in range(rows):
        row_str = ", ".join(map(str, matrix[i]))
        matrix_rows.append(row_str)
    return "{\n    " + ",\n    ".join(matrix_rows) + "\n}"


def generate_expected_matrix_output(matrix_name, matrix_str, rows_expr, cols_expr):
    matrix_data_name = f"SIMPLE_KF_{matrix_name}_data"
    matrix_name_full = f"SIMPLE_KF_{matrix_name}"

    return [
        f"static matrix_data_t {matrix_data_name}[{rows_expr} * {cols_expr}] = {matrix_str};",
        f"static matrix_t {matrix_name_full} = {{{rows_expr}, {cols_expr}, {matrix_data_name}}};",
    ]


# fmt: off
@pytest.mark.parametrize(
    "config_path, matrix_name, rows_expr, cols_expr",
    [
        (SIMPLE_CONFIG_PATH, "F", "SIMPLE_KF_NUM_STATES", "SIMPLE_KF_NUM_STATES"),
        (SIMPLE_CONFIG_PATH, "H", "SIMPLE_KF_NUM_MEASUREMENTS", "SIMPLE_KF_NUM_STATES"),
        (SIMPLE_CONFIG_PATH, "Q", "SIMPLE_KF_NUM_STATES", "SIMPLE_KF_NUM_STATES"),
        (SIMPLE_CONFIG_PATH, "R", "SIMPLE_KF_NUM_MEASUREMENTS", "SIMPLE_KF_NUM_MEASUREMENTS"),
        (SIMPLE_CONFIG_PATH, "P_init", "SIMPLE_KF_NUM_STATES", "SIMPLE_KF_NUM_STATES"),
        (SIMPLE_CONFIG_PATH, "X_init", "SIMPLE_KF_NUM_STATES", "(1U)"),
        (SIMPLE_CONFIG_PATH_WITH_CONTROL, "B", "SIMPLE_KF_NUM_STATES", "SIMPLE_KF_NUM_CONTROLS"),
    ],
)
# fmt: on
def test_config_matrix(config_path, matrix_name, rows_expr, cols_expr):
    config = load_config(config_path)
    generated_config = KalmanFilterConfigGenerator(config)

    matrix = getattr(generated_config.config, matrix_name)
    matrix_str = format_matrix_with_newlines(matrix, cols_expr)

    expected_matrix_output = generate_expected_matrix_output(
        matrix_name, matrix_str, rows_expr, cols_expr
    )

    generated_definitions_str = "\n".join(generated_config.generated_config_definitions)

    expected_output_str = "\n".join(expected_matrix_output)
    assert expected_output_str in generated_definitions_str


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


@pytest.mark.parametrize(
    "config_path, struct_type, struct_key",
    [
        (
            SIMPLE_CONFIG_PATH,
            "measurement",
            "simple_kf_measurement_S",
        ),
        (
            SIMPLE_CONFIG_PATH_WITH_CONTROL,
            "measurement",
            "simple_kf_measurement_S",
        ),
    ],
)
def test_measurement_structure_definition(config_path, struct_type, struct_key):
    config = load_config(config_path)
    generated_config = KalmanFilterConfigGenerator(config)

    expected_measurement_structure = [
        "typedef struct {",
        "\tmatrix_data_t data[SIMPLE_KF_NUM_MEASUREMENTS];",
        "\tbool valid[SIMPLE_KF_NUM_MEASUREMENTS];",
        f"}} {struct_key};",
    ]

    expected_structure_str = "\n".join(expected_measurement_structure)
    generated_structure_str = "\n".join(
        generated_config.generated_structure_definitions[struct_type]
    )

    assert expected_structure_str in generated_structure_str


def test_control_structure_definition():
    config = load_config(SIMPLE_CONFIG_PATH_WITH_CONTROL)
    generated_config = KalmanFilterConfigGenerator(config)

    control_struct_name = "simple_kf_control_S"  # Updated to lowercase

    expected_control_structure = [
        "typedef struct {",
        "\tmatrix_data_t data[SIMPLE_KF_NUM_CONTROLS];",
        f"}} {control_struct_name};",
    ]

    expected_structure_str = "\n".join(expected_control_structure)
    generated_structure_str = "\n".join(
        generated_config.generated_structure_definitions["control"]
    )

    assert expected_structure_str in generated_structure_str


@pytest.mark.parametrize(
    "config_path",
    [SIMPLE_CONFIG_PATH, SIMPLE_CONFIG_PATH_WITH_CONTROL],
)
def test_function_headers(config_path):
    with open(config_path) as f:
        config = json.load(f)

        simple_kf_config = config[0]
        simple_kf_config_converted = KalmanFilterConfig(simple_kf_config)

        generated_config = KalmanFilterConfigGenerator(simple_kf_config_converted)

        measurement_struct_name = f"{simple_kf_config['name']}_measurement_S"

        expected_function_headers = [
            f"kf_error_E {simple_kf_config['name']}_init(void);",
            f"kf_error_E {simple_kf_config['name']}_update({measurement_struct_name} const * const measurement);",
        ]

        if config_path == SIMPLE_CONFIG_PATH_WITH_CONTROL:
            control_struct_name = f"{simple_kf_config['name']}_control_S"
            expected_function_headers.append(
                f"kf_error_E {simple_kf_config['name']}_predict({control_struct_name} const * const control);"
            )
        else:
            expected_function_headers.append(
                f"kf_error_E {simple_kf_config['name']}_predict(void);"
            )

        for header in expected_function_headers:
            assert header in generated_config.generated_function_headers


def assert_function_definition(expected_definition, generated_definitions):
    generated_definitions_str = "\n".join(generated_definitions)
    expected_definition_str = "\n".join(expected_definition)
    assert expected_definition_str in generated_definitions_str


@pytest.mark.parametrize("config_path", [SIMPLE_CONFIG_PATH])
def test_init_function_definition(config_path):
    config = load_config(config_path)
    generated_config = KalmanFilterConfigGenerator(config)

    kf_name = config.raw_config["name"]
    data_struct_name = generated_config.generated_structure_names["filter_data"]
    config_struct_name = generated_config.generated_structure_names["filter_config"]

    init_function_definition = [
        f"kf_error_E {kf_name}_init(void) {{",
        f"\treturn kf_init(&{data_struct_name}, &{config_struct_name});",
        "}",
    ]

    assert_function_definition(
        init_function_definition, generated_config.generated_function_definitions
    )


@pytest.mark.parametrize("config_path", [SIMPLE_CONFIG_PATH])
def test_measurement_function_definition(config_path):
    config = load_config(config_path)
    generated_config = KalmanFilterConfigGenerator(config)

    kf_name = config.raw_config["name"]
    data_struct_name = generated_config.generated_structure_names["filter_data"]

    measurement_function_definition = [
        f"kf_error_E {kf_name}_update({kf_name}_measurement_S const * const measurement) {{",
        f"\tmatrix_t Z = {{SIMPLE_KF_NUM_MEASUREMENTS, 1U, measurement->data}};",
        f"\treturn kf_update(&{data_struct_name}, &Z, &measurement->valid, SIMPLE_KF_NUM_MEASUREMENTS);",
        "}",
    ]

    assert_function_definition(
        measurement_function_definition, generated_config.generated_function_definitions
    )


@pytest.mark.parametrize(
    "config_path", [SIMPLE_CONFIG_PATH, SIMPLE_CONFIG_PATH_WITH_CONTROL]
)
def test_control_function_definition(config_path):
    config = load_config(config_path)
    generated_config = KalmanFilterConfigGenerator(config)

    kf_name = config.raw_config["name"]
    data_struct_name = generated_config.generated_structure_names["filter_data"]

    if config_path == SIMPLE_CONFIG_PATH_WITH_CONTROL:
        control_function_definition = [
            f"kf_error_E {kf_name}_predict({kf_name}_control_S const * const control) {{",
            f"\tmatrix_t U = {{SIMPLE_KF_NUM_CONTROLS, 1U, control->data}};",
            f"\treturn kf_predict(&{data_struct_name}, &U);",
            "}",
        ]
    else:
        control_function_definition = [
            f"kf_error_E {kf_name}_predict(void) {{",
            f"\treturn kf_predict(&{data_struct_name}, NULL);",
            "}",
        ]

    assert_function_definition(
        control_function_definition, generated_config.generated_function_definitions
    )
