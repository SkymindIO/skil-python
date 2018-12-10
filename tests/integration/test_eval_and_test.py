#!/usr/bin/env python
import pytest
import sys

import keras
from keras.datasets import mnist

import json

import numpy as np

import skil
from skil import Skil, WorkSpace, Experiment, Deployment, Model as SkilModel, Service
import skil_client
from six.moves import range

import uuid

def test_eval_and_test():
    with open('.skil', 'r') as f:
        skil_conf = json.load(f)

    # Connect to SKIL and create an experiment for storing our model experiments.
    skil_server = Skil(
        host=skil_conf['host'],
        port=skil_conf['port'],
        user_id=skil_conf['username'], 
        password=skil_conf['password'])
    work_space = skil.get_workspace_by_id(None, skil_server, skil_conf['workspace_id'])
    experiment = skil.get_experiment_by_id(work_space, skil_conf['experiment_id'])
    model = skil.get_model_by_id(None, experiment=experiment, id=skil_conf['model_id']) 

    deployment = None
    if skil_conf['deployment_id'] == '':
        deployment = Deployment(skil_server, "mnist_models")
        skil_conf['deployment_id'] = deployment.id
        with open('.skil', 'w') as f:
            json.dump(skil_conf, f)
    else:
        deployment = skil.get_deployement_by_id(skil_server, skil_conf['deployment_id'])

    service = None
    try:
        service = model.deploy(deployment=deployment)
    except Exception:
        print('Service with name already exists reusing...')
        service = Service(skil_server, "mnist", deployment, {})

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_test = x_test.reshape(10000, 784)
    x_test = x_test.astype('float32')
    x_test /= 255

    num_correct = 0
    for i in range(10000):
        digit = x_test[i]
        label = y_test[i]

        result = service.predict_single(digit)
        predicted = np.argmax(result)

        if predicted == label:
            num_correct += 1
        print("Predicted: %s Actual: %s Same: %s" % (predicted, label, predicted == label))

    print("Test Accuracy: %s" % (float(num_correct) / 10000,))

if __name__ == '__main__':
    pytest.main([__file__])
