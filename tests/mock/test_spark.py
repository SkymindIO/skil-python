import pytest
from skil.spark import *


def test_pa_config():
    pa = ParameterAveraging(8, 32)
    conf = pa.to_json()

    retrieved = ParameterAveraging.from_json(conf)

    assert retrieved.to_json() == conf


def test_ps_config():
    ps = ParameterSharing(8, 32)
    conf = ps.to_json()

    retrieved = ParameterSharing.from_json(conf)

    assert retrieved.to_json() == conf


if __name__ == '__main__':
    pytest.main([__file__])
