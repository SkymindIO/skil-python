import skil
from skil.services import *

import skil_client
from skil_client.rest import ApiException as api_exception
import time
import os
import uuid


class Model:
    """SKIL wrapper for DL4J, Keras, TensorFlow and other models

    SKIL has a robust model storage, serving, and import system for supporting major 
    deep learning libraries.
    SKIL can be used for end-to-end training, configuration, and deployment of models 
    or alternatively you can import models into SKIL.

    # Arguments
        model: Model file path or  model instance
        model_id: integer. Unique id for model. If `None`, a unique id will be generated.
        name: string. Name for the model.
        version: integer. Version of the model. Defaults to 1.
        experiment: `Experiment` instance. If `None`, an `Experiment` object will be created internally.
        labels: string. Labels for this model
        verbose: boolean. If `True`, prints api response.
        create: boolean. Internal. Do not use.
    """

    def __init__(self, model=None, model_id=None, name=None, version=None, experiment=None,
                 labels='', verbose=False, create=True):
        if create:
            if isinstance(model, str) and os.path.isfile(model):
                model_file_name = model
            else:
                if hasattr(model, 'save'):
                    model_file_name = 'temp_model.h5'
                    if os.path.isfile(model_file_name):
                        os.remove(model_file_name)
                    model.save(model_file_name)
                else:
                    raise Exception('Invalid model: ' + str(model))
            if not experiment:
                self.skil = skil.Skil.from_config()
                self.work_space = skil.workspaces.WorkSpace(self.skil)
                self.experiment = skil.experiments.Experiment(self.work_space)
            else:
                self.experiment = experiment
                self.work_space = experiment.work_space
                self.skil = self.work_space.skil
            self.skil.upload_model(os.path.join(os.getcwd(), model_file_name))

            self.model_path = self.skil.get_model_path(model_file_name)
            self.id = model_id if model_id else str(uuid.uuid1())
            self.name = name if name else model_file_name
            self.version = version if version else 1

            self.evaluations = {}

            self.deployment = None
            self.model_deployment = None

            add_model_instance_response = self.skil.api.add_model_instance(
                self.skil.server_id,
                skil_client.ModelInstanceEntity(
                    uri=self.model_path,
                    model_id=self.id,
                    model_labels=labels,
                    model_name=name,
                    model_version=self.version,
                    created=int(round(time.time() * 1000)),
                    experiment_id=self.experiment.id
                )
            )
            if verbose:
                self.skil.printer.pprint(add_model_instance_response)
        else:
            self.experiment = experiment
            self.work_space = experiment.work_space
            self.skil = self.work_space.skil
            assert model_id is not None
            self.id = model_id
            model_entity = self.skil.api.get_model_instance(self.skil.server_id,
                                                            self.id)
            self.name = model_entity.model_name
            self.version = model_entity.model_version
            self.model_path = model_entity.uri

        self.service = None

    def delete(self):
        """Deletes the model
        """
        try:
            self.skil.api.delete_model_instance(self.skil.server_id, self.id)
        except api_exception as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_model_instance: %s\n" % e)

    def add_evaluation(self, accuracy, eval_id=None, name=None, version=None):
        eval_version = version if version else 1
        eval_id = eval_id if eval_id else str(uuid.uuid1())
        eval_name = name if name else str(uuid.uuid1())

        eval_response = self.skil.api.add_evaluation_result(
            self.skil.server_id,
            skil_client.EvaluationResultsEntity(
                evaluation="",  # TODO: what is this?
                created=int(round(time.time() * 1000)),
                eval_name=eval_name,
                model_instance_id=self.id,
                accuracy=float(accuracy),
                eval_id=eval_id,
                eval_version=eval_version
            )
        )
        self.evaluations[eval_id] = eval_response

    def deploy(self, deployment=None, start_server=True, scale=1, input_names=None,
               output_names=None, verbose=True):
        """Deploys the model

        # Arguments:
            deployment: `Deployment` instance.
            start_server: boolean. If `True`, the service is immedietely started.
            scale: integer. Scale-out for deployment.
            input_names: list of strings. Input variable names of the model.
            output_names: list of strings. Output variable names of the model.
            verbose: boolean. If `True`, api response will be printed.

        # Returns:
            `Service` instance.
        """
        if not deployment:
            deployment = skil.Deployment(skil=self.skil, name=self.name)

        uris = ["{}/model/{}/default".format(deployment.name, self.name),
                "{}/model/{}/v1".format(deployment.name, self.name)]

        if not self.service:
            deploy_model_request = skil_client.ImportModelRequest(
                name=self.name,
                scale=scale,
                file_location=self.model_path,
                model_type="model",
                uri=uris,
                input_names=input_names,
                output_names=output_names)

            # TODO: why ".response"? Doesn't make sense.
            self.deployment = deployment.response

            models = self.skil.api.models(self.deployment.id)
            deployed_model = [m for m in models if m.name == self.name]
            if deployed_model:
                self.model_deployment = deployed_model[0]
            else:
                self.model_deployment = self.skil.api.deploy_model(
                    self.deployment.id, deploy_model_request)
                if verbose:
                    self.skil.printer.pprint(self.model_deployment)

            self.service = Service(self.skil, self,
                                   self.deployment, self.model_deployment)
        if start_server:
            self.service.start()
        return self.service

    def undeploy(self):
        """Un-deploy the model.
        """
        try:
            self.skil.api.delete_model(self.deployment.id, self.id)
        except skil_client.rest.ApiException as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_model_instance: %s\n" % e)


def get_model_by_id(experiment, model_id):
    return Model(model_id=model_id, experiment=experiment, create=False)


class Transform(Model):
    """SKIL wrapper for for preprocessing (transform) steps. Currently only
    supports `TransformProcess` instances from pydatavec or their serialized
    versions (JSON format).

    # Arguments
        transform: pydatavec.TransformProcess or TransformProcess JSON
        transform_id: integer. Unique id for the transform. If `None`, a unique id will be generated.
        transform_type: Type of the SKIL transform. Choose from "CSV", "image" or "array"
        name: string. Name for the transform.
        version: integer. Version of the transform. Defaults to 1.
        experiment: `Experiment` instance. If `None`, an `Experiment` object will be created internally.
        labels: string. Labels associated with the workspace, useful for searching (comma seperated).
        verbose: boolean. If `True`, prints api response.
        create: boolean. Internal. Do not use.
    """

    def __init__(self, transform=None, transform_type='CSV', transform_id=None, name=None,
                 version=None, experiment=None,
                 labels='', verbose=False, create=True):
        if create:
            if isinstance(transform, str) and os.path.isfile(transform):
                transform_file_name = transform
            else:
                if hasattr(transform, 'to_java'):
                    transform_file_name = 'temp_transform.json'
                    if os.path.isfile(transform_file_name):
                        os.remove(transform_file_name)
                    with open(transform_file_name, 'w') as f:
                        f.write(transform.to_java().toJson())
                else:
                    raise Exception(
                        'Invalid TransformProcess: ' + str(transform))
            if not experiment:
                self.skil = skil.Skil.from_config()
                self.work_space = skil.workspaces.WorkSpace(self.skil)
                self.experiment = skil.experiments.Experiment(self.work_space)
            else:
                self.experiment = experiment
                self.work_space = experiment.work_space
                self.skil = self.work_space.skil
            self.skil.upload_model(os.path.join(
                os.getcwd(), transform_file_name))

            self.model_path = self.skil.get_model_path(transform_file_name)
            self.id = transform_id if transform_id else str(uuid.uuid1())
            self.name = name if name else transform_file_name
            self.version = version if version else 1

            self.evaluations = {}

            self.deployment = None
            self.model_deployment = None

            add_model_instance_response = self.skil.api.add_model_instance(
                self.skil.server_id,
                skil_client.ModelInstanceEntity(
                    uri=self.model_path,
                    model_id=self.id,
                    model_labels=labels,
                    model_name=name,
                    model_version=self.version,
                    created=int(round(time.time() * 1000)),
                    experiment_id=self.experiment.id
                )
            )
            if verbose:
                self.skil.printer.pprint(add_model_instance_response)
        else:
            self.experiment = experiment
            self.work_space = experiment.work_space
            self.skil = self.work_space.skil
            assert transform_id is not None
            self.id = transform_id
            model_entity = self.skil.api.get_model_instance(self.skil.server_id,
                                                            self.id)
            self.name = model_entity.model_name
            self.version = model_entity.model_version
            self.model_path = model_entity.uri

        self.transform_type = transform_type
        self.service = None

    def deploy(self, deployment=None, start_server=True, scale=1, input_names=None,
               output_names=None, verbose=True):
        """Deploys the model

        # Arguments:
            deployment: `Deployment` instance.
            start_server: boolean. If `True`, the service is immedietely started.
            scale: integer. Scale-out for deployment.
            input_names: list of strings. Input variable names of the model.
            output_names: list of strings. Output variable names of the model.
            verbose: boolean. If `True`, api response will be printed.

        # Returns:
            `Service` instance.
        """
        if not deployment:
            deployment = skil.Deployment(skil=self.skil, name=self.name)

        uris = ["{}/datavec/{}/default".format(deployment.name, self.name),
                "{}/datavec/{}/v1".format(deployment.name, self.name)]

        if not self.service:
            deploy_model_request = skil_client.ImportModelRequest(
                name=self.name,
                scale=scale,
                file_location=self.model_path,
                model_type="transform",
                uri=uris,
                input_names=input_names,
                output_names=output_names)

            self.deployment = deployment.response

            models = self.skil.api.models(self.deployment.id)
            deployed_model = [m for m in models if m.name == self.name]
            if deployed_model:
                self.model_deployment = deployed_model[0]
            else:
                self.model_deployment = self.skil.api.deploy_model(
                    self.deployment.id, deploy_model_request)
                if verbose:
                    self.skil.printer.pprint(self.model_deployment)

            if self.transform_type == 'CSV':
                self.service = TransformCsvService(
                    self.skil, self, self.deployment, self.model_deployment)
            elif self.transform_type == 'array':
                self.service = TransformArrayService(
                    self.skil, self, self.deployment, self.model_deployment)
            elif self.transform_type == 'image':
                self.service = TransformImageService(
                    self.skil, self, self.deployment, self.model_deployment)

        if start_server:
            self.service.start()
        return self.service


def get_transform_by_id(experiment, transform_id):
    return Transform(transform_id=transform_id, experiment=experiment, create=False)
