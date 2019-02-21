import pytest
import mock
from skil.jobs import *
from skil.spark import ParameterAveraging
import skil


def test_base_training_job():
    skil_server = skil.Skil()
    model = skil.Model('keras_mnist.h5')

    res = skil.resources.compute.EMR(
        skil_server, 'name', 'region', 'creds', 'id')
    conf = TrainingJobConfiguration(
        model, 10, "acc", "EvalDSP", res, res, './', "DSP")
    distributed_config = ParameterAveraging(8, 32)

    # TODO "jobArgs" does not get recognize"
    # job = TrainingJob(skil_server, conf, distributed_config)
    # job._training_job_args()
    # with pytest.raises(Exception):
    #     job.run()


def test_base_inference_job():
    skil_server = skil.Skil()
    model = skil.Model('keras_mnist.h5')

    res = skil.resources.compute.EMR(
        skil_server, 'name', 'region', 'creds', 'id')
    conf = InferenceJobConfiguration(model, 32, res, res, './', "DSP")

    # job = InferenceJob(skil_server, conf)
    # job.inference_config()
    # with pytest.raises(Exception):
    #     job.run()


if __name__ == '__main__':
    pytest.main([__file__])
