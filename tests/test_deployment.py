import sys
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock
from skil import Deployment


@mock.patch('skil.Skil')
def test_skil_default_model(Skil):
    skil_server = Skil()
    deployment = Deployment(skil_server)
