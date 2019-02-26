import pytest
import skil

def test_skil_creation():
    sk = skil.Skil()


def test_work_space_creation():
    sk = skil.Skil()
    work_space = skil.WorkSpace(sk)
    work_space.delete()


def test_experiment_creation():
    sk = skil.Skil()
    work_space = skil.WorkSpace(sk)
    exp = skil.Experiment(work_space)
    work_space.delete()
    exp.delete()


def test_deployment_creation():
    sk = skil.Skil()
    dep = skil.Deployment(sk)
    dep.delete()


def test_model_creation_1():
    model = skil.Model('keras_mnist.h5')
    model.delete()

def test_model_creation_2():
    sk = skil.Skil()
    work_space = skil.WorkSpace(sk)
    exp = skil.Experiment(work_space)
    model = skil.Model('keras_mnist.h5', experiment=exp)
    work_space.delete()
    exp.delete()
    model.delete()


def test_transform_creation_1():
    transform = skil.Transform('iris_tp.json')
    transform.delete()


def test_transform_creation_2():
    sk = skil.Skil()
    work_space = skil.WorkSpace(sk)
    exp = skil.Experiment(work_space)
    transform = skil.Transform('iris_tp.json', experiment=exp)
    transform.add_evaluation(0.42)
    work_space.delete()
    exp.delete()
    transform.delete()


def test_service_creation():
    sk = skil.Skil()
    work_space = skil.WorkSpace(sk)
    exp = skil.Experiment(work_space)
    model = skil.Model('keras_mnist.h5', experiment=exp)
    model.add_evaluation(0.95)

    dep = skil.Deployment(sk)
    model.deploy(dep)
    work_space.delete()
    exp.delete()
    model.delete()
    dep.delete()

if __name__ == '__main__':
    pytest.main([__file__])
