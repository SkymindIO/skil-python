import skil_client
from skil_client.rest import ApiException as api_exception
import uuid
import json
import yaml
import keras
import os
import sys
import shutil

from .base import Skil
from .workspaces import get_workspace_by_id, WorkSpace
from .utils.io import serialize_config, deserialize_config


class Experiment:
    """Experiments in SKIL are useful for defining different model configurations, 
    encapsulating training of models, and carrying out different data cleaning tasks.

    Experiments have a one-to-one relationship with Notebooks and have their own 
    storage mechanism for saving different model configurations when seeking a best 
    candidate.

    # Arguments:
        work_space: `WorkSpace` instance. If `None` a workspace will be created.
        experiment_id: integer. Unique id for workspace. If `None`, a unique id will be generated.
        name: string. Name for the experiment.
        description: string. Description for the experiment.
        verbose: boolean. If `True`, api response will be printed.
        skil_server: Optional `Skil` instance, used when create is false.
        create: boolean. If `True` a new experiment will be created.
    """

    def __init__(self, work_space=None, experiment_id=None, name='experiment',
                 description='experiment', verbose=False, skil_server=None, create=True,
                 *args, **kwargs):

        if create:
            if not work_space:
                if skil_server:
                    self.skil = skil_server
                else:
                    self.skil = Skil.from_config()
                work_space = WorkSpace(self.skil)
            self.work_space = work_space
            self.skil = self.work_space.skil
            self.id = experiment_id if experiment_id else work_space.id + \
                "_experiment_" + str(uuid.uuid1())
            self.name = name
            experiment_entity = skil_client.ExperimentEntity(
                experiment_id=self.id,
                experiment_name=name,
                experiment_description=description,
                model_history_id=self.work_space.id
            )

            add_experiment_response = self.skil.api.add_experiment(
                self.skil.server_id,
                experiment_entity
            )
            self.experiment_entity = experiment_entity

            if verbose:
                self.skil.printer.pprint(add_experiment_response)
        else:
            experiment_entity = skil_server.api.get_experiment(
                skil_server.server_id,
                experiment_id
            )
            self.experiment_entity = experiment_entity
            self.work_space = work_space
            self.id = experiment_id
            self.name = experiment_entity.experiment_name

        # only used when experiment is retrieved through notebook
        self.skil_environment = None

    def get_config(self):
        return {
            'experiment_id': self.id,
            'experiment_name': self.name,
            'workspace_id': self.work_space.id
        }

    def save(self, file_name, file_format='json'):
        config = self.get_config()
        serialize_config(config, file_name, file_format)

    @classmethod
    def load(cls, file_name, skil_server=None):
        config = deserialize_config(file_name)

        skil_server = Skil.from_config() if skil_server is None else skil_server
        experiment = get_experiment_by_id(skil_server, config['experiment_id'])
        experiment.name = config['experiment_name']
        return experiment

    def delete(self):
        """Deletes the experiment.
        """
        try:
            api_response = self.skil.api.delete_experiment(
                self.work_space.id, self.id)
            self.skil.printer.pprint(api_response)
        except api_exception as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_experiment: %s\n" % e)

    @classmethod
    def current_skil_experiment(cls, skil_server, zeppelin_context):
        """Get the SKIL experiment associated with this Zeppelin notebook.

        # Arguments:
            skil_server: a `Skil` instance
            zeppelin_context: a `ZeppelinContext` instance

        # Return value:
            A `skil.Experiment`
        """
        jvm_skil_context = zeppelin_context.sc._jvm.io.skymind.zeppelin.utils.SkilContext
        context = jvm_skil_context()
        experiment_id = context.experimentId(zeppelin_context.z)

        result = get_experiment_by_id(skil_server, experiment_id)
        result.skil_environment = zeppelin_context.sc._jvm.io.skymind.skil.service.SKILEnvironment
        return result

    def _models_path(self):
        if not self.skil_environment:
            raise Exception("No SKIL environment class found. You need to retrieve" +
                            "your experiment through current_skil_experiment to use" +
                            "the save_model or copy_model functionality. Only use" +
                            "this when working with SKIL's Zeppelin notebooks.")

        service_path = self.skil_environment.skilServiceWorkingDirFile().toString()
        storage_path = os.path.join(service_path, "storage")
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        models_path = os.path.join(storage_path, "models")
        if not os.path.exists(models_path):
            os.mkdir(models_path)

        return models_path

    def save_model(self, model):
        """Save the model into SKIL's managed models directory. Currently
        only supports saving in-memory Keras models

        # Arguments:
            model: The model to save

        # Return value:
            The path of the saved model.
        """
        if isinstance(model, keras.models.Model):
            models_path = self._models_path()
            file_path = os.path.join(models_path, str(uuid.uuid1()) + '.h5')

            if isinstance(file_path, unicode):
                file_path = file_path.encode(sys.getfilesystemencoding())
            model.save(str(file_path))
            return file_path
        else:
            raise NotImplementedError("Only Keras models currently supported.")

    def copy_model(self, source_path, model_type):
        """Copy a model file (tensorflow or ONNX) to the managed model directory.

        # Arguments:
            path: The path to the model you want to copy
            model_type: The type of model. Currently either 'tensorflow' or 'onnx'

        # Return value:
            The path of the saved model
        """
        if model_type.lower() == 'tensorflow' or model_type.lower() == 'tf':
            dest_path = os.path.join(
                self._models_path(), str(uuid.uuid1()) + '.pb')
        elif model_type.lower() == 'onnx':
            dest_path = os.path.join(
                self._models_path(), str(uuid.uuid1()) + '.onnx')
        else:
            raise NotImplementedError(
                'Only TensorFlow and ONNX model types are supported.')

        shutil.copyfile(source_path, dest_path)
        return dest_path


def get_experiment_by_id(skil_server, experiment_id):
    """Get experiment by ID

    # Arguments:
        skil: `Skil` server instance
        experiment: string, experiment ID
    """
    return Experiment(skil_server=skil_server, experiment_id=experiment_id, create=False)
