from unittest.mock import patch, MagicMock
from skil import WorkSpace, Experiment, Model, Deployment


@patch('skil.Skil')
def test_skil_default_model(Skil):
    model = Model('dummy_file_name')
    model.add_evaluation(id='eval', name='eval', version=1, accuracy=0.93)
    model.deploy()
    # model.serve() TODO need to mock api response for this one