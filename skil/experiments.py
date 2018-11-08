import skil_client


class Experiment:
    """Experiments in SKIL are useful for defining different model configurations, encapsulating training of models, and carrying out different data cleaning tasks.

    Experiments have a one-to-one relationship with Notebooks and have their own storage mechanism for saving different model configurations when seeking a best candidate.

    # Arguments:
    work_space: `WorkSpace` instance.
    id: integer. Unique id for workspace. If `None`, a unique id will be generated.
    name: string. Name for the experiment.
    description: string. Description for the experiment.
    verbose: boolean. If `True`, api response will be printed.
    """
    def __init__(self, work_space=None, id=None, name='test', description='test', verbose=False, create=True):
        if create:
            self.work_space = work_space
            self.skil = self.work_space.skil
            self.id = id if id else work_space.id + "_experiment"
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
                id
            )
            self.experiment_entity = experiment_entity
            self.work_space = work_space
            self.id = id
            self.name = experiment_entity.experiment_name

    def delete(self):
        """Deletes the experiment.
        """
        try:
            api_response = self.skil.api.delete_experiment(
                self.work_space.id, self.id)
            self.skil.printer.pprint(api_response)
        except skil_client.rest.ApiException as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_experiment: %s\n" % e)

def get_experiment_by_id(work_space, id):
    return Experiment(work_space=work_space, id=id, create=False)
