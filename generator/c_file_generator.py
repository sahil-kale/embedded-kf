import numpy as np

try:
    from generator.ingestor import KalmanFilterConfig
except ImportError:
    from ingestor import KalmanFilterConfig


class KalmanFilterConfigGenerator:
    def __init__(self, config: KalmanFilterConfig):
        self.config = config
        filter_name = config.raw_config["name"].upper()

        self.num_states_expr = f"{filter_name}_NUM_STATES"
        self.num_measurements_expr = f"{filter_name}_NUM_MEASUREMENTS"
        self.num_controls_expr = f"{filter_name}_NUM_CONTROLS"

        self.generated_preprocessor_defines = self.generate_preprocessor_defines(
            filter_name, config.num_states, config.num_measurements, config.num_controls
        )

        matrices = self.build_matrix_list()
        self.generated_config_definitions = self.add_matrix_definitions(matrices)

        storage_variables = self.build_storage_variables_list()
        self.generated_storage_definitions = self.add_storage_definitions(
            filter_name, storage_variables
        )

        self.generated_struct_config_definition = (
            self.generate_struct_config_definition(filter_name, storage_variables)
        )

    def generate_preprocessor_defines(
        self, name: str, num_states: int, num_measurements: int, num_controls: int
    ):
        return [
            f"#define {name}_NUM_STATES ({num_states}U)",
            f"#define {name}_NUM_MEASUREMENTS ({num_measurements}U)",
            f"#define {name}_NUM_CONTROLS ({num_controls}U)",
        ]

    def generate_config_definitions(
        self,
        name: str,
        matrix_name: str,
        matrix_data: np.array,
        rows_name: str,
        cols_name: str,
    ):
        matrix_flattened_str = (
            "{" + ", ".join(str(x) for x in matrix_data.flatten()) + "}"
        )
        return [
            f"static matrix_data_t {name}_{matrix_name}_data[{rows_name} * {cols_name}] = {matrix_flattened_str};",
            f"static matrix_t {name}_{matrix_name} = {{{rows_name}, {cols_name}, {name}_{matrix_name}_data}};",
        ]

    def add_matrix_definitions(self, matrices: list):
        matrix_definitions = []
        for matrix_name, matrix_data, rows_expr, cols_expr in matrices:
            matrix_definitions.extend(
                self.generate_config_definitions(
                    self.config.raw_config["name"].upper(),
                    matrix_name,
                    matrix_data,
                    rows_expr,
                    cols_expr,
                )
            )
        return matrix_definitions

    def build_matrix_list(self):
        """Generates the list of matrices based on the configuration."""
        # fmt: off
        matrices = [
            ("F", self.config.F, self.num_states_expr, self.num_states_expr),
            ("H", self.config.H, self.num_measurements_expr, self.num_states_expr),
            ("Q", self.config.Q, self.num_states_expr, self.num_states_expr),
            ("R", self.config.R, self.num_measurements_expr, self.num_measurements_expr),
            ("P_init", self.config.P_init, self.num_states_expr, self.num_states_expr),
            ("X_init", self.config.X_init, self.num_states_expr, "(1U)"),
        ]
        # fmt: on

        if self.config.num_controls > 0:
            matrices.append(
                ("B", self.config.B, self.num_states_expr, self.num_controls_expr)
            )
        return matrices

    def build_storage_variables_list(self):
        """Generates the list of storage variables based on the configuration."""
        # fmt: off
        return [
            ("X_matrix_storage", self.num_states_expr, "(1U)"),
            ("P_matrix_storage", self.num_states_expr, self.num_states_expr),
            ("temp_X_hat_matrix_storage", self.num_states_expr, "(1U)"),
            ("temp_Bu_matrix_storage", self.num_states_expr, "(1U)"),
            ("temp_Z_matrix_storage", self.num_measurements_expr, "(1U)"),
            ("H_temp_storage", self.num_measurements_expr, self.num_states_expr),
            ("R_temp_storage", self.num_measurements_expr, self.num_measurements_expr),
            ("P_Ht_storage", self.num_states_expr, self.num_measurements_expr),
            ("Y_matrix_storage", self.num_measurements_expr, "(1U)"),
            ("S_matrix_storage", self.num_measurements_expr, self.num_measurements_expr),
            ("S_inv_matrix_storage", self.num_measurements_expr, self.num_measurements_expr),
            ("K_matrix_storage", self.num_states_expr, self.num_measurements_expr),
            ("K_H_storage", self.num_states_expr, self.num_states_expr),
            ("K_H_P_storage", self.num_states_expr, self.num_states_expr),
        ]
        # fmt: on

    def add_storage_definitions(self, name, storage_variables: list):
        return [
            f"static matrix_data_t {name}_{var}[{rows} * {cols}] = {{0}};"
            for var, rows, cols in storage_variables
        ]

    def generate_struct_config_definition(self, name: str, storage_variables: list):
        struct_config = [
            f"const kf_config_S {name}_kf_config = {{",
            "\t// Matrix Configuration Variables",
            f"\t.X_init = &{name}_X_init,",
            f"\t.F = &{name}_F,",
            f"\t.B = &{name}_B," if self.config.num_controls > 0 else "\t.B = NULL,",
            f"\t.Q = &{name}_Q,",
            f"\t.P_init = &{name}_P_init,",
            f"\t.H = &{name}_H,",
            f"\t.R = &{name}_R,",
            "\t// Storage variables",
        ]

        struct_config.extend(
            f"\t.{var} = {{{rows} * {cols}, {name}_{var}}},"
            for var, rows, cols in storage_variables
        )

        struct_config.append("};")
        return struct_config

    def write_to_file(self, output_file_path: str):
        with open(output_file_path, "w") as output_file:
            output_file.write('#include "kalman.h"\n\n')
            output_file.write("\n".join(self.generated_preprocessor_defines) + "\n\n")
            output_file.write("\n".join(self.generated_config_definitions) + "\n\n")
            output_file.write("\n".join(self.generated_storage_definitions) + "\n\n")
            output_file.write(
                "\n".join(self.generated_struct_config_definition) + "\n\n"
            )
