from unittest.mock import patch
from skil import WorkSpace, Experiment


@patch('skil.Skil')
def test_experiment(Skil):
    skil_server = Skil()
    ws = WorkSpace(skil_server)
    experiment = Experiment(ws)
