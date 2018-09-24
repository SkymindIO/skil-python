from unittest.mock import patch, MagicMock
from skil import WorkSpace, Experiment, Model, Deployment


@patch('skil.Skil')
def test_work_space(Skil):
    skil_server = Skil()
    ws = WorkSpace(skil_server)
