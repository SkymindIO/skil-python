import pytest
import skil


def test_experiment_serde():
    exp = skil.Experiment()
    exp.save('exp.json')

    recov = skil.Experiment.load('exp.json')

    assert recov.get_config() == exp.get_config()


def test_deployment_serde():
    dep = skil.Deployment()
    dep.save('dep.json')

    recov = skil.Deployment.load('dep.json')

    assert recov.get_config() == dep.get_config()


if __name__ == '__main__':
    pytest.main([__file__])
