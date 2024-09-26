from ctypes import *
from argparse import ArgumentParser
import numpy as np
import json
import os
import sys

# Add the package above to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from generator.ingestor import KalmanFilterConfig
from generator.file_content_generator import KalmanFilterConfigGenerator

# Generic KalmanFilterSimulator which works with KalmanFilterConfigGenerator
class KalmanFilterSimulator:
    def __init__(self, lib_path, config_generator):
        self.config_generator = config_generator
        self.kalman_lib = cdll.LoadLibrary(lib_path)

        # Extract relevant config details
        self.num_measurements = config_generator.config.num_measurements
        self.num_controls = config_generator.config.num_controls

        # Get function names dynamically from the config generator
        self.init_function_name = f"{self.config_generator.filter_name}_init"
        self.predict_function_name = f"{self.config_generator.filter_name}_predict"
        self.update_function_name = f"{self.config_generator.filter_name}_update"

        # Dynamically create ctypes structures based on the configuration
        self.MeasurementStructure = self._create_measurement_structure()
        self.ControlStructure = self._create_control_structure()

        # Define the function signatures dynamically based on configuration
        self._define_function_signatures()

    def _create_measurement_structure(self):
        # Create ctypes structure for measurement data based on num_measurements
        class MeasurementStructure(Structure):
            _fields_ = [
                ("data", c_float * self.num_measurements),
                ("valid", c_bool * self.num_measurements)
            ]
        return MeasurementStructure

    def _create_control_structure(self):
        # Create ctypes structure for control data based on num_controls
        class ControlStructure(Structure):
            _fields_ = [
                ("data", c_float * self.num_controls)
            ]
        return ControlStructure

    def _define_function_signatures(self):
        # Define the function signatures for the Kalman filter functions

        # init function dynamically from the config
        try:
            init_func = getattr(self.kalman_lib, self.init_function_name)
            init_func.restype = c_int
            self.kalman_lib.init = init_func  # Alias the function for usage
        except AttributeError:
            raise AttributeError(f"{self.init_function_name} not found in the shared library.")

        # predict function dynamically from the config
        if self.num_controls > 0:
            try:
                predict_func = getattr(self.kalman_lib, self.predict_function_name)
                predict_func.restype = c_int
                predict_func.argtypes = [POINTER(self.ControlStructure)]
                self.kalman_lib.predict = predict_func  # Alias the function for usage
            except AttributeError:
                raise AttributeError(f"{self.predict_function_name} not found in the shared library.")

        # update function dynamically from the config
        try:
            update_func = getattr(self.kalman_lib, self.update_function_name)
            update_func.restype = c_int
            update_func.argtypes = [POINTER(self.MeasurementStructure)]
            self.kalman_lib.update = update_func  # Alias the function for usage
        except AttributeError:
            raise AttributeError(f"{self.update_function_name} not found in the shared library.")

    def initialize_filter(self):
        # Call the Kalman filter init function
        result = self.kalman_lib.init()
        if result != 0:
            print("Kalman filter initialization failed!")
        else:
            print("Kalman filter initialized successfully!")

    def predict(self, control_input):
        if self.num_controls > 0:
            # Create control structure and fill with control input data
            control_struct = self.ControlStructure()
            control_struct.data[:] = control_input

            # Call the predict function
            result = self.kalman_lib.predict(byref(control_struct))
            if result != 0:
                print("Kalman filter prediction failed!")
            else:
                print("Kalman filter prediction successful!")

    def update(self, measurement_data, validity):
        # Create measurement structure and fill with measurement data and validity mask
        measurement_struct = self.MeasurementStructure()
        measurement_struct.data[:] = measurement_data
        measurement_struct.valid[:] = validity

        # Call the update function
        result = self.kalman_lib.update(byref(measurement_struct))
        if result != 0:
            print("Kalman filter update failed!")
        else:
            print("Kalman filter update successful!")

    def run(self):
        # Example control input and measurement data
        control_input = np.array([0.1, 0.2, -0.1], dtype=np.float32) if self.num_controls > 0 else None
        measurement_data = np.array([1.0, 0.5, 0.25], dtype=np.float32)
        validity = [True, False, True]

        # Initialize the Kalman filter
        self.initialize_filter()

        # Run the predict step
        if control_input is not None:
            self.predict(control_input)

        # Run the update step
        self.update(measurement_data, validity)


if __name__ == '__main__':
    parser = ArgumentParser()

    # Provide the path to the Kalman shared library
    parser.add_argument('kalman_lib', type=str, help="Path to the shared Kalman filter library (e.g., libkalman.so)")
    parser.add_argument('config_file', type=str, help="Path to the Kalman filter configuration file")

    args = parser.parse_args()

    with open(args.config_file) as f:
        config = json.load(f)

        config = config[0]

        # Load the Kalman filter configuration
        ingested_config = KalmanFilterConfig(config)

        # Create a KalmanFilterConfigGenerator object
        config_generator = KalmanFilterConfigGenerator(ingested_config)

        # Create the KalmanFilterSimulator object
        simulator = KalmanFilterSimulator(args.kalman_lib, config_generator)

        # Run the Kalman filter simulation
        simulator.run()
