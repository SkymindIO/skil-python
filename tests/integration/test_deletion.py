import pytest
import skil


work_space = None  # because number of workspaces is limited


def _get_ws():
    global work_space
    if work_space is None:
        work_space = skil.WorkSpace(skil.Skil())
    return work_space


def test_work_space_deletion():
    sk = skil.Skil()
    work_space = skil.WorkSpace(sk)
    work_space.delete()


def test_experiment_deletion():
    ws =_get_ws()
    exp = skil.Experiment(ws)
    exp.delete()


if __name__ == '__main__':
    pytest.main([__file__])
