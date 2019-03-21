import pytest
import skil
import uuid
import os

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


def test_work_space_by_id():
    global work_space
    global work_space_id
    sk = _get_sk()
    work_space = skil.WorkSpace(sk, name='test_ws')
    ws_id = work_space.id
    work_space_id = ws_id
    work_space2 = skil.get_workspace_by_id(sk, ws_id)
    assert work_space.name == work_space2.name


def test_experiment_by_id():
    ws = _get_ws()
    exp = skil.Experiment(ws, name='test_exp')
    exp_id = exp.id
    exp2 = skil.get_experiment_by_id(ws.skil, exp_id)
    assert exp.name == exp2.name


def test_deployment_by_id():
    sk = _get_sk()
    dep = skil.Deployment(sk, name='test_dep' + str(uuid.uuid1())[:6])
    dep_id = dep.id
    dep2 = skil.get_deployment_by_id(sk, dep_id)
    assert dep.name == dep2.name


def test_model_by_id():
    ws = _get_ws()
    exp = skil.Experiment(ws, name='test_exp2')
    with open('model.h5', 'w') as f:
        f.write('')
    model = skil.Model('model.h5', name='test_model', experiment=exp)
    model_id = model.id
    model2 = skil.get_model_by_id(exp, model_id)
    assert model.name == model2.name
    os.remove('model.h5')


def test_transform_by_id():
    ws = _get_ws()
    exp = skil.Experiment(ws, name='test_transform')
    transform = skil.Transform('iris_tp.json')
    transform_id = transform.id
    tf_2 = skil.get_transform_by_id(transform_id, "CSV", exp)
    assert tf_2.name == transform.name


if __name__ == '__main__':
    pytest.main([__file__])
