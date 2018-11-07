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


def test_work_space_deletion():
    sk = _get_sk()
    work_space = skil.WorkSpace(sk)
    work_space.delete()


def test_experiment_deletion():
    ws =_get_ws()
    exp = skil.Experiment(ws)
    exp.delete()


if __name__ == '__main__':
    pytest.main([__file__])
