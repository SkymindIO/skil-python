import skil_client
from skil_client.rest import ApiException as api_exception
import uuid
import json
from .base import Skil
from .workspaces import get_workspace_by_id, WorkSpace


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
        create: boolean. If `True` a new experiment will be created.
    """

    def __init__(self, work_space=None, experiment_id=None, name='experiment',
                 description='experiment', verbose=False, create=True,
                 *args, **kwargs):
        if create:
            if not work_space:
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
            experiment_entity = work_space.skil.api.get_experiment(
                work_space.skil.server_id,
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

    def save(self, file_name):
        config = self.get_config()
        with open(file_name, 'w') as f:
            json.dump(config, f)

    @classmethod
    def load(cls, file_name):
        with open(file_name, 'r') as f:
            config = json.load(f)

        skil_server = Skil()
        work_space = get_workspace_by_id(skil_server, config['workspace_id'])
        return get_experiment_by_id(work_space, config['experiment_id'])

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


def get_experiment_by_id(work_space, experiment_id):
    return Experiment(work_space=work_space, experiment_id=experiment_id, create=False)
