import pytest

from skil.utils.io import serialize_config, deserialize_config
from skil import Experiment

import sys
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock


MOCK_CONFIG = {
    'experiment_id': 'foo',
    'experiment_name': 'bar',
    'workspace_id': 'baz'
}


@mock.patch('skil.Skil')
def test_experiment_json_serde(Skil):
    file_name = "./mock.json"
    serialize_config(MOCK_CONFIG, file_name, 'json')

    config = deserialize_config(file_name)
    assert config == MOCK_CONFIG
    exp = Experiment.load(file_name, Skil())
    assert exp.id == 'foo'


@mock.patch('skil.Skil')
def test_experiment_yaml_serde(Skil):
    file_name = "./mock.yml"
    serialize_config(MOCK_CONFIG, file_name, 'yaml')

    config = deserialize_config(file_name)
    assert config == MOCK_CONFIG
    exp = Experiment.load(file_name, Skil())
    assert exp.id == 'foo'


@mock.patch('skil.Skil')
def test_failed_serde(Skil):
    file_name = "./mock.fail"

    with pytest.raises(Exception):
        serialize_config(MOCK_CONFIG, file_name, 'foo')

    with open(file_name, 'w') as f:
        f.write('foobar')

    with pytest.raises(Exception):
        conf = deserialize_config(file_name)


if __name__ == '__main__':
    pytest.main([__file__])
