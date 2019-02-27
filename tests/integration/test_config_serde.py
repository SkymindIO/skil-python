import pytest
import skil


def test_experiment_serde():
    exp = skil.Experiment(name='foo')
    exp.save('exp.json')

    recov = skil.Experiment.load('exp.json')

    assert recov.get_config() == exp.get_config()


def test_model_serde():
    model = skil.Model('keras_mnist.h5', name='bar')
    model.save('model.json')

    recov = skil.Model.load('model.json')

    assert recov.get_config() == model.get_config()


def test_transform_serde():
    transform = skil.Transform('iris_tp.json', 'baz')
    transform.save('transform.json')

    recov = skil.Transform.load('transform.json')

    assert recov.get_config() == transform.get_config()


def test_deployment_serde():
    dep = skil.Deployment()
    dep.save('dep.json')

    recov = skil.Deployment.load('dep.json')

    assert recov.get_config() == dep.get_config()


def test_service_serde():
    dep = skil.Deployment()
    model = skil.Model('keras_mnist.h5', name='bar')
    service = model.deploy(dep)
    service.save('service.json')

    recov = skil.Service.load('service.json')

    assert recov.get_config() == service.get_config()


if __name__ == '__main__':
    pytest.main([__file__])
