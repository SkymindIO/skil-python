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


def test_work_space_creation():
    global work_space
    work_space = skil.WorkSpace(sk)


def test_transform_creation_1():
    model = skil.Transform('iris_tp.json')


def test_transform_creation_2():
    ws = _get_ws()
    exp = skil.Experiment(ws)
    model = skil.Transform('iris_tp.json', experiment=exp)


def test_transform_service_creation():
    ws = _get_ws()
    exp = skil.Experiment(ws)
    model = skil.Transform('iris_tp.json', experiment=exp)
    dep = skil.Deployment(ws.skil)
    model.deploy(dep)


if __name__ == '__main__':
    pytest.main([__file__])
