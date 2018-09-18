import pytest
from skil import Skil, WorkSpace, Experiment, Model

def test_base_api():
    model_path = './tf_graph.pb'

    # TODO: retrieve default model history server id.
    skil_server = Skil(model_server_id='dec0bbde-bf81-45cf-b223-f88c24d0ff99')
    skil_server.upload_model(model_path)

    ws = WorkSpace(skil_server, 'jupyter_ws')
    experiment = Experiment(ws, 'test_exp')

    model = Model(experiment, model_path, id='model_id', name='model', version=1)
    model.add_evaluation(id='eval', name='eval', version=1, accuracy=0.93)
