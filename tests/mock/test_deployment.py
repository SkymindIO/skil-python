import pytest
import sys
from skil import Deployment
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock


@mock.patch('skil.Skil')
def test_skil_default_model(Skil):
    skil_server = Skil()
    deployment = Deployment(skil_server)


if __name__ == '__main__':
    pytest.main([__file__])
