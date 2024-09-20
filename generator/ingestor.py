import numpy as np


# Create a class of exceptions
class InvalidConfigException(Exception):
    pass


# Create an exception for bad dimensions
class InvalidDimensionsException(Exception):
    def __init__(self, key: str, expected_dims: tuple, actual_dims: tuple):
        self.key = key
        self.expected_dims = expected_dims
        self.actual_dims = actual_dims
        self.message = (
            f"Expected {key} to have dimensions {expected_dims}, but got {actual_dims}"
        )
        super().__init__(self.message)


# Define the supported keys with their required status and expected dimensions
NUM_STATES_STR = "num_states"
NUM_MEASUREMENTS_STR = "num_measurements"
NUM_CONTROLS_STR = "num_controls"

# fmt: off
supported_keys = [
    {"key": "F", "required": True, "expected_dims": (NUM_STATES_STR, NUM_STATES_STR)},
    {"key": "Q", "required": True, "expected_dims": (NUM_STATES_STR, NUM_STATES_STR)},
    {"key": "H", "required": True, "expected_dims": (NUM_MEASUREMENTS_STR, NUM_STATES_STR)},
    {"key": "R", "required": True, "expected_dims": (NUM_MEASUREMENTS_STR, NUM_MEASUREMENTS_STR)},
    {"key": "P_init", "required": True, "expected_dims": (NUM_STATES_STR, NUM_STATES_STR)},
    {"key": "X_init", "required": True, "expected_dims": (NUM_STATES_STR,)},
    {"key": "B", "required": False, "expected_dims": (NUM_STATES_STR, NUM_CONTROLS_STR)},
    {"key": "name", "required": True},
]
# fmt: on

# Collect the set of all supported keys and required keys
supported_keys_set = {item["key"] for item in supported_keys}
required_keys_set = {item["key"] for item in supported_keys if item["required"]}


class KalmanFilterConfig:
    def __init__(self, config: dict):
        self.raw_config = config

        # Check that all required keys are present in the config
        for key in required_keys_set:
            if key not in config:
                raise InvalidConfigException(f"Missing required key: {key}")

        # Check that there are no unknown keys in the config
        for key in config:
            if key not in supported_keys_set:
                raise InvalidConfigException(f"Unknown key: {key}")

        # List of keys corresponding to matrices that need conversion
        matrix_keys = ["F", "Q", "H", "R", "P_init", "X_init"]

        if "B" in config:
            matrix_keys.append("B")

        # Convert matrices to NumPy arrays and assign to class attributes
        for key in matrix_keys:
            setattr(self, key, np.array(config[key], dtype=np.float32))

        # After matrices are converted, you can access their shapes
        self.num_states = self.X_init.shape[0]
        self.num_measurements = self.H.shape[0]

        if "B" in config:
            self.num_controls = self.B.shape[1]
        else:
            self.num_controls = 0
            self.B = None

        # Proceed with generating expected dimensions and verifying them
        expected_dims_dict = self._generate_expected_dims(matrix_keys)
        self._verify_dimensions(expected_dims_dict)

        # Make an exception for X_init and reshape it to size (num_states, 1)
        self.X_init = self.X_init.reshape(self.num_states, 1)

    def _generate_expected_dims(self, matrix_keys):
        """
        Generate a dictionary mapping each key in matrix_keys to its expected dimensions,
        replacing placeholders with actual values.
        """
        expected_dims_dict = {}
        for key in matrix_keys:
            # Find the item in supported_keys with this key
            item = next((item for item in supported_keys if item["key"] == key), None)
            if item and "expected_dims" in item:
                expected_dims = item["expected_dims"]
                # Replace placeholders with actual values
                expected_dim_values = []
                for dim in expected_dims:
                    if dim == NUM_STATES_STR:
                        expected_dim_values.append(self.num_states)
                    elif dim == NUM_MEASUREMENTS_STR:
                        expected_dim_values.append(self.num_measurements)
                    elif dim == NUM_CONTROLS_STR:
                        expected_dim_values.append(self.num_controls)
                    else:
                        expected_dim_values.append(
                            dim
                        )  # In case of integers or other literals
                expected_dims_dict[key] = tuple(expected_dim_values)
        return expected_dims_dict

    def _verify_dimensions(self, expected_dims_dict):
        """
        Verify that the actual dimensions of the matrices match the expected dimensions.
        """
        for key, expected_dim in expected_dims_dict.items():
            actual_dim = getattr(self, key).shape
            if actual_dim != expected_dim:
                raise InvalidDimensionsException(key, expected_dim, actual_dim)
