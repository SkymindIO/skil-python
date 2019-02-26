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
    work_space = skil.WorkSpace(sk)
    work_space.delete()


def test_experiment_creation():
    ws = _get_ws()
    exp = skil.Experiment(work_space)
    ws.delete()
    exp.delete()


def test_deployment_creation():
    sk = _get_sk()
    dep = skil.Deployment(sk)


def test_model_creation_1():
    model = skil.Model('keras_mnist.h5')
    model.delete()

def test_model_creation_2():
    ws = _get_ws()
    exp = skil.Experiment(ws)
    model = skil.Model('keras_mnist.h5', experiment=exp)
    ws.delete()
    exp.delete()
    model.delete()


def test_service_creation():
    ws = _get_ws()
    exp = skil.Experiment(ws)
    model = skil.Model('keras_mnist.h5', experiment=exp)
    model.add_evaluation(0.95)

    dep = skil.Deployment(ws.skil)
    model.deploy(dep)
    ws.delete()
    exp.delete()
    model.delete()

if __name__ == '__main__':
    pytest.main([__file__])
