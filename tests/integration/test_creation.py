import pytest
import skil


work_space = None  # because number of workspaces is limited
_sk = None


def _get_sk():
    global _sk
    if _sk is None:
        _sk = skil.Skil()
    return _sk


def _get_ws():
    global work_space
    if work_space is not None:
        return work_space
    sk = _get_sk()
    work_space = skil.WorkSpace(sk)
    return work_space


def test_skil_creation():
    global sk
    sk = skil.Skil()


def test_work_sapce_creation():
    global work_space
    global work_space_id
    work_sapce = skil.WorkSpace(sk)


def test_experiment_creation():
    ws = _get_ws()
    exp = skil.Experiment(work_space)


def test_deployment_creation():
    sk = _get_sk()
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
