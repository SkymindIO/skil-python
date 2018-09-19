import pytest
from skil import Skil, WorkSpace, Experiment, Model, Deployment


def test_base_api():
    model_path = './tf_graph.pb'

    skil_server = Skil()
    skil_server.upload_model(model_path)

    ws = WorkSpace(skil_server, 'jupyter_ws')
    experiment = Experiment(ws, 'test_exp')

    model = Model(experiment, model_path, id='model_id', name='model', version=1)
    model.add_evaluation(id='eval', name='eval', version=1, accuracy=0.93)

    deployment = Deployment(skil_server, 'test_deployment')
    model.deploy(deployment)
