import pytest
import mock
from skil.jobs import *
from skil.spark import ParameterAveraging
import skil


def test_inference_job_config():
    res = skil.resources.compute.EMR(None, 'name', 'region', 'creds', 'id', 'res_id', False)

    conf = InferenceJobConfiguration(None, 32, res, res, './', None)
    assert conf.batch_size == 32


def test_training_job_config():
    res = skil.resources.compute.EMR(None, 'name', 'region', 'creds', 'id', 'res_id', False)

    conf = TrainingJobConfiguration(None, 10, None, None, res, res, './', None)
    assert conf.num_epochs == 10


def test_base_job():
    job = Job()
    assert job.job_id == None


if __name__ == '__main__':
    pytest.main([__file__])
