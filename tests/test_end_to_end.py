from unittest.mock import patch
from skil import WorkSpace, Experiment, Model, Deployment


@patch('skil.Skil')
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