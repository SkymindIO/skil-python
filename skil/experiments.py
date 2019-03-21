import skil_client
from skil_client.rest import ApiException as api_exception
import uuid
import json
import yaml

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
    def current_skil_experiment(cls, skil_server, sc, zeppelin_context):
        """Get the SKIL experiment associated with this Zeppelin notebook.

        # Arguments:
            skil_server: a `Skil` instance
            spark_context: a `SparkContext` instance
            zeppelin_context: a `ZeppelinContext` instance

        # Return value:
            A `skil.Experiment`
        """
        jvm_skil_context = sc._jvm.io.skymind.zeppelin.utils.SkilContext
        context = jvm_skil_context()
        skil_environment = sc._jvm.io.skymind.skil.service.SKILEnvironment
        # self.ModelInstanceEntity = sc._jvm.io.skymind.modelproviders.history.model.ModelInstanceEntity
        # Nd4j = sc._jvm.org.nd4j.linalg.factory.Nd4j
        # self.Evaluation = sc._jvm.org.deeplearning4j.eval.Evaluation

        experiment_id = context.experimentId(zeppelin_context.z)

        result = get_experiment_by_id(skil_server, experiment_id)
        result.jvm_skil_context = jvm_skil_context
        result.context = context
        result.skil_environment = skil_environment
        return result


def get_experiment_by_id(skil_server, experiment_id):
    return Experiment(skil_server=skil_server, experiment_id=experiment_id, create=False)
