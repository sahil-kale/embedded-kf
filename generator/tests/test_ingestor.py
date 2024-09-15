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


@pytest.mark.parametrize("key_to_remove", ["F", "Q", "H", "R", "P", "name"])
def test_missing_key(key_to_remove: str):
    # load the simple config
    with open(SIMPLE_CONFIG_PATH) as f:
        config = json.load(f)

        simple_kf_config = config[0]

        # remove the parameterization key
        simple_kf_config.pop(key_to_remove)

        # test that the exception is raised
        with pytest.raises(InvalidConfigException):
            create_kalman_filter_config_from_dict(simple_kf_config)


def test_unknown_key():
    # load the simple config
    with open(SIMPLE_CONFIG_PATH) as f:
        config = json.load(f)

        simple_kf_config = config[0]

        # add an unknown key
        simple_kf_config["unknown_key"] = 1

        # test that the exception is raised
        with pytest.raises(InvalidConfigException):
            create_kalman_filter_config_from_dict(simple_kf_config)


@pytest.mark.parametrize("matrix_to_edit", ["F", "Q", "H", "R", "P"])
def test_matrix_that_cannot_be_converted_to_numpy(matrix_to_edit):
    # load the simple config
    with open(SIMPLE_CONFIG_PATH) as f:
        config = json.load(f)

        simple_kf_config = config[0]

        # add a matrix that cannot be converted to numpy
        simple_kf_config[matrix_to_edit] = "not a matrix"

        # test that the exception is raised
        with pytest.raises(ValueError):
            create_kalman_filter_config_from_dict(simple_kf_config)


@pytest.mark.parametrize("matrix_with_invalid_dims", ["F", "Q", "H", "R", "P"])
def test_matrix_with_wrong_shape(matrix_with_invalid_dims: str):
    # load the simple config
    with open(SIMPLE_CONFIG_PATH) as f:
        config = json.load(f)

        simple_kf_config = config[0]

        # add a matrix with invalid dimensions
        simple_kf_config[matrix_with_invalid_dims] = [[1, 2], [3, 4], [5, 6]]

        # test that the exception is raised
        with pytest.raises(InvalidDimensionsException):
            create_kalman_filter_config_from_dict(simple_kf_config)


@pytest.mark.parametrize(
    "filter_to_load", [SIMPLE_CONFIG_PATH, SIMPLE_CONFIG_PATH_WITH_CONTROL]
)
def test_nominal_simple_filter_load(filter_to_load):
    # load the simple config
    with open(filter_to_load) as f:
        config = json.load(f)

        simple_kf_config = config[0]

        # test that the exception is raised
        kf = create_kalman_filter_config_from_dict(simple_kf_config)

        assert kf.num_states == 2
        assert kf.num_measurements == 1
        assert kf.config["name"] == simple_kf_config["name"]

        if filter_to_load == SIMPLE_CONFIG_PATH_WITH_CONTROL:
            assert kf.num_controls == 1
