from generator.file_content_generator import KalmanFilterConfigGenerator


class FileWriter:
    def __init__(self, generator, c_output_file_path: str, h_output_file_path: str):
        self.generated_filter_static_data_struct = (
            generator.generated_filter_static_data_struct
        )
        self.generated_config_definitions = generator.generated_config_definitions
        self.generated_storage_definitions = generator.generated_storage_definitions
        self.generated_struct_config_definition = (
            generator.generated_struct_config_definition
        )
        self.generated_function_definitions = generator.generated_function_definitions
        self.generated_preprocessor_defines = generator.generated_preprocessor_defines
        self.generated_structure_definitions = generator.generated_structure_definitions
        self.generated_function_headers = generator.generated_function_headers

        self.write_to_file(c_output_file_path, h_output_file_path)

    def write_to_file(self, c_output_file_path: str, h_output_file_path: str):
        # Write to .c file
        self._write_c_file(c_output_file_path, h_output_file_path)

        # Write to .h file
        self._write_h_file(h_output_file_path)

    def _write_c_file(self, c_output_file_path: str, h_output_file_path: str):
        """Helper function to write the .c file."""
        with open(c_output_file_path, "w") as output_file:
            self._write_c_includes(output_file, h_output_file_path)
            self._write_c_definitions(output_file)

    def _write_h_file(self, h_output_file_path: str):
        """Helper function to write the .h file."""
        with open(h_output_file_path, "w") as output_file:
            self._write_h_includes(output_file)
            self._write_h_preprocessor_defines(output_file)
            self._write_h_struct_definitions(output_file)
            self._write_h_function_headers(output_file)

    def _write_c_includes(self, output_file, h_output_file_path):
        """Helper to write includes for the .c file."""
        header_file_name = h_output_file_path.split("/")[-1]
        includes = [
            '#include "kalman.h"',
            "#define EXTERN_INLINE_MATRIX STATIC_INLINE",
            '#include "matrix.h"',
            f'#include "{header_file_name}"',
        ]
        output_file.write("\n".join(includes) + "\n\n")

    def _write_c_definitions(self, output_file):
        """Helper to write definitions for the .c file."""
        sections = [
            self.generated_filter_static_data_struct,
            "\n".join(self.generated_config_definitions),
            "\n".join(self.generated_storage_definitions),
            "\n".join(self.generated_struct_config_definition),
            "/* Function Definitions */",
            "\n".join(self.generated_function_definitions),
        ]
        output_file.write("\n\n".join(sections) + "\n\n")

    def _write_h_includes(self, output_file):
        """Helper to write includes for the .h file."""
        output_file.write('#include "kalman.h"\n\n')

    def _write_h_preprocessor_defines(self, output_file):
        """Helper to write preprocessor defines for the .h file."""
        output_file.write("/* Preprocessor Defines */\n")
        output_file.write("\n".join(self.generated_preprocessor_defines) + "\n\n")

    def _write_h_struct_definitions(self, output_file):
        """Helper to write struct definitions for the .h file."""
        output_file.write("/* Struct Definitions */\n")
        for struct_definition in self.generated_structure_definitions.values():
            output_file.write("\n".join(struct_definition) + "\n\n")

    def _write_h_function_headers(self, output_file):
        """Helper to write function headers for the .h file."""
        output_file.write("/* Function Headers */\n")
        for header in self.generated_function_headers.values():
            output_file.write(header["comment"])
            output_file.write(header["str"] + "\n\n")
