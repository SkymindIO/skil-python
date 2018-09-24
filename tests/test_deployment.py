from unittest.mock import patch
from skil import Deployment


@patch('skil.Skil')
def test_skil_default_model(Skil):
    skil_server = Skil()
    deployment = Deployment(skil_server)