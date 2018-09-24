import sys
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock
from skil import WorkSpace, Experiment, Model, Deployment


@mock.patch('skil.Skil')
def test_e2e(Skil):
    model_path = './dummy.pb'

    skil_server = Skil()
    skil_server.upload_model(model_path)

    ws = WorkSpace(skil_server, 'jupyter_ws')
    experiment = Experiment(ws, 'test_exp')

    model = Model(model_path, experiment)
    model.add_evaluation(accuracy=0.93)

    deployment = Deployment(skil_server, 'test_deployment')
    model.deploy(deployment)