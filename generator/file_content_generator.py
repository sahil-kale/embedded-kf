import numpy as np

try:
    from generator.ingestor import KalmanFilterConfig
except ImportError:
    from ingestor import KalmanFilterConfig


class KalmanFilterConfigGenerator:
    def __init__(self, config: KalmanFilterConfig):
        self.config = config
        self.filter_name = config.raw_config["name"]
        filter_name_uppercase = self.filter_name.upper()

        self.generated_structure_names = self.generate_structure_names()

        self.error_enum = "kf_error_E"
        self.preprocessor_define_expressions = (
            self.generate_preprocessor_define_expressions(filter_name_uppercase)
        )
        self.preprocessor_define_expansions = (
            self.generate_preprocessor_define_expansions()
        )

        self.generated_preprocessor_defines = self.generate_preprocessor_defines()

        matrices = self.build_matrix_list()
        self.generated_filter_static_data_struct = (
            self.generate_static_filter_data_struct()
        )

        self.generated_config_definitions = self.add_matrix_definitions(matrices)
        storage_variables = self.build_storage_variables_list()

        self.generated_storage_definitions = self.add_storage_definitions(
            filter_name_uppercase, storage_variables
        )
        self.generated_struct_config_definition = (
            self.generate_struct_config_definition(
                filter_name_uppercase, storage_variables
            )
        )

        self.generated_function_headers = self.generate_function_headers()
        self.generated_structure_definitions = self.generate_structure_definitions()
        self.generated_function_definitions = self.generate_function_definitions()

    def generate_preprocessor_define_expressions(self, filter_name_uppercase):
        return {
            "num_states": f"{filter_name_uppercase}_NUM_STATES",
            "num_measurements": f"{filter_name_uppercase}_NUM_MEASUREMENTS",
            "num_controls": f"{filter_name_uppercase}_NUM_CONTROLS",
        }

    def generate_preprocessor_define_expansions(self):
        return {
            "num_states": f"{self.config.num_states}U",
            "num_measurements": f"{self.config.num_measurements}U",
            "num_controls": f"{self.config.num_controls}U",
        }

    def generate_static_filter_data_struct(self):
        return f"static kf_data_S {self.generated_structure_names['filter_data']};"

    def generate_function_definitions(self):
        init_function = self.generate_init_function()
        measurement_update_function = self.generate_measurement_update_function()

        generated_function_definitions = [init_function, measurement_update_function]

        if self.config.num_controls > 0:
            predict_function = self.generate_predict_function(with_control=True)
        else:
            predict_function = self.generate_predict_function(with_control=False)
        generated_function_definitions.append(predict_function)

        return generated_function_definitions

    def generate_init_function(self):
        return (
            f"{self.error_enum} {self.filter_name}_init(void) {{\n"
            f"\treturn kf_init(&{self.generated_structure_names['filter_data']}, "
            f"&{self.generated_structure_names['filter_config']});\n}}"
        )

    def generate_measurement_update_function(self):
        # fmt: off
        return (
            f"{self.error_enum} {self.filter_name}_update({self.generated_structure_names['measurement']}_S const * const measurement) {{\n"
            f"\tmatrix_t Z = {{{self.preprocessor_define_expressions['num_measurements']}, 1U, measurement->data}};\n"
            f"\treturn kf_update(&{self.generated_structure_names['filter_data']}, &Z, &measurement->valid, {self.preprocessor_define_expressions['num_measurements']});\n}}"
        )
        # fmt: on

    def generate_predict_function(self, with_control):
        if with_control:
            # fmt: off
            return (
                f"{self.error_enum} {self.filter_name}_predict({self.generated_structure_names['control']}_S const * const control) {{\n"
                f"\tmatrix_t U = {{{self.preprocessor_define_expressions['num_controls']}, 1U, control->data}};\n"
                f"\treturn kf_predict(&{self.generated_structure_names['filter_data']}, &U);\n}}"
            )
            # fmt: on
        else:
            # fmt: off
            return (
                f"{self.error_enum} {self.filter_name}_predict(void) {{\n"
                f"\treturn kf_predict(&{self.generated_structure_names['filter_data']}, NULL);\n}}"
            )
            # fmt: on

    def generate_structure_names(self):
        return {
            "measurement": f"{self.filter_name}_measurement",
            "control": f"{self.filter_name}_control",
            "state": f"{self.filter_name}_state",
            "filter_data": f"{self.filter_name.upper()}_data",
            "filter_config": f"{self.filter_name.upper()}_kf_config",
        }

    def generate_function_headers(self):
        # fmt: off
        headers = [
            f"{self.error_enum} {self.filter_name}_init(void);",
            f"{self.error_enum} {self.filter_name}_update({self.generated_structure_names['measurement']}_S const * const measurement);",
        ]
        if self.config.num_controls > 0:
            headers.append(
                f"{self.error_enum} {self.filter_name}_predict({self.generated_structure_names['control']}_S const * const control);"
            )
        else:
            headers.append(f"{self.error_enum} {self.filter_name}_predict(void);")
        # fmt: on
        return headers

    def generate_structure_definitions(self):
        measurement_struct = self.generate_measurement_struct_definition()
        control_struct = self.generate_control_struct_definition()

        return {
            "measurement": measurement_struct,
            "control": control_struct,
        }

    def generate_measurement_struct_definition(self):
        return [
            "typedef struct {",
            f"\tmatrix_data_t data[{self.preprocessor_define_expressions['num_measurements']}];",
            f"\tbool valid[{self.preprocessor_define_expressions['num_measurements']}];",
            f"}} {self.generated_structure_names['measurement']}_S;",
        ]

    def generate_control_struct_definition(self):
        return [
            "typedef struct {",
            f"\tmatrix_data_t data[{self.preprocessor_define_expressions['num_controls']}];",
            f"}} {self.generated_structure_names['control']}_S;",
        ]

    def generate_preprocessor_defines(self):
        return [
            f"#define {self.preprocessor_define_expressions[key]} ({self.preprocessor_define_expansions[key]})"
            for key in self.preprocessor_define_expressions
        ]

    def format_matrix_with_newlines(self, matrix: np.ndarray) -> str:
        rows, cols = matrix.shape
        matrix_rows = []
        for i in range(rows):
            row_str = ", ".join(map(str, matrix[i]))
            matrix_rows.append(row_str)
        return "{\n    " + ",\n    ".join(matrix_rows) + "\n}"

    def generate_config_definitions(
        self,
        name: str,
        matrix_name: str,
        matrix_data: np.array,
        rows_name: str,
        cols_name: str,
    ):
        matrix_flattened_str = self.format_matrix_with_newlines(matrix_data)
        # fmt: off
        return [
            f"static matrix_data_t {name}_{matrix_name}_data[{rows_name} * {cols_name}] = {matrix_flattened_str};",
            f"static matrix_t {name}_{matrix_name} = {{{rows_name}, {cols_name}, {name}_{matrix_name}_data}};",
        ]
        # fmt: on

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
        # fmt: off
        matrices = [
            ("F", self.config.F, self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_states"]),
            ("H", self.config.H, self.preprocessor_define_expressions["num_measurements"], self.preprocessor_define_expressions["num_states"]),
            ("Q", self.config.Q, self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_states"]),
            ("R", self.config.R, self.preprocessor_define_expressions["num_measurements"], self.preprocessor_define_expressions["num_measurements"]),
            ("P_init", self.config.P_init, self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_states"]),
            ("X_init", self.config.X_init, self.preprocessor_define_expressions["num_states"], "(1U)"),
        ]
        # fmt: on
        if self.config.num_controls > 0:
            matrices.append(
                (
                    "B",
                    self.config.B,
                    self.preprocessor_define_expressions["num_states"],
                    self.preprocessor_define_expressions["num_controls"],
                )
            )
        return matrices

    def build_storage_variables_list(self):
        # fmt: off
        return [
            ("X_matrix_storage", self.preprocessor_define_expressions["num_states"], "(1U)"),
            ("P_matrix_storage", self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_states"]),
            ("temp_X_hat_matrix_storage", self.preprocessor_define_expressions["num_states"], "(1U)"),
            ("temp_Bu_matrix_storage", self.preprocessor_define_expressions["num_states"], "(1U)"),
            ("temp_Z_matrix_storage", self.preprocessor_define_expressions["num_measurements"], "(1U)"),
            ("H_temp_storage", self.preprocessor_define_expressions["num_measurements"], self.preprocessor_define_expressions["num_states"]),
            ("R_temp_storage", self.preprocessor_define_expressions["num_measurements"], self.preprocessor_define_expressions["num_measurements"]),
            ("P_Ht_storage", self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_measurements"]),
            ("Y_matrix_storage", self.preprocessor_define_expressions["num_measurements"], "(1U)"),
            ("S_matrix_storage", self.preprocessor_define_expressions["num_measurements"], self.preprocessor_define_expressions["num_measurements"]),
            ("S_inv_matrix_storage", self.preprocessor_define_expressions["num_measurements"], self.preprocessor_define_expressions["num_measurements"]),
            ("K_matrix_storage", self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_measurements"]),
            ("K_H_storage", self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_states"]),
            ("K_H_P_storage", self.preprocessor_define_expressions["num_states"], self.preprocessor_define_expressions["num_states"]),
        ]
        # fmt: on

    def add_storage_definitions(self, name, storage_variables: list):
        return [
            f"static matrix_data_t {name}_{var}[{rows} * {cols}] = {{0}};"
            for var, rows, cols in storage_variables
        ]

    def generate_struct_config_definition(self, name: str, storage_variables: list):
        # fmt: off
        struct_config = [
            f"const kf_config_S {self.generated_structure_names['filter_config']} = {{",
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
        # fmt: on

        struct_config.extend(
            f"\t.{var} = {{{rows} * {cols}, {name}_{var}}},"
            for var, rows, cols in storage_variables
        )

        struct_config.append("};")
        return struct_config

    def write_to_file(self, c_output_file_path: str, h_output_file_path: str):
        with open(c_output_file_path, "w") as output_file:
            output_file.write('#include "kalman.h"\n\n')
            header_file_name = h_output_file_path.split("/")[-1]
            output_file.write(f'#include "{header_file_name}"\n\n')
            output_file.write(self.generated_filter_static_data_struct + "\n\n")
            output_file.write("\n".join(self.generated_config_definitions) + "\n\n")
            output_file.write("\n".join(self.generated_storage_definitions) + "\n\n")
            output_file.write(
                "\n".join(self.generated_struct_config_definition) + "\n\n"
            )
            output_file.write("/* Function Definitions */\n")
            output_file.write("\n".join(self.generated_function_definitions) + "\n\n")

        with open(h_output_file_path, "w") as output_file:
            output_file.write('#include "kalman.h"\n\n')
            output_file.write("/* Preprocessor Defines */\n")
            output_file.write("\n".join(self.generated_preprocessor_defines) + "\n\n")
            output_file.write("/* Function Headers */\n")
            output_file.write("\n".join(self.generated_function_headers) + "\n\n")
            output_file.write("/* Struct Definitions */\n")
            for (
                struct_name,
                struct_definition,
            ) in self.generated_structure_definitions.items():
                output_file.write("\n".join(struct_definition) + "\n\n")
