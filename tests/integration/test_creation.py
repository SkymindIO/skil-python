import pytest
import skil


work_space = None  # because number of workspaces is limited


def _get_ws():
    global work_space
    if work_space is None:
        work_space = skil.WorkSpace(skil.Skil())
    return work_space


def test_skil_creation():
    sk = skil.Skil()


def test_work_sapce_creation():
    global work_space
    sk = skil.Skil()
    work_sapce = skil.WorkSpace(sk)


def test_experiment_creation():
    ws =_get_ws()
    exp = skil.Experiment(work_space)


def test_deployment_creation():
    sk = skil.Skil()
    dep = skil.Deployment(sk)


def test_model_creation_1():
    model = skil.Model('model.h5')


def test_model_creation_2():
    ws = _get_ws()
    exp = skil.Experiment(ws)
    model = skil.Model('model.h5', experiment=exp)


def test_service_creation():
    ws = _get_ws()
    exp = skil.Experiment(ws)
    model = skil.Model('model.h5', experiment=exp)
    dep = skil.Deployment(ws.skil)
    model.deploy(dep)


if __name__ == '__main__':
    pytest.main([__file__])
