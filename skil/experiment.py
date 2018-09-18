import skil_client


class Experiment():

    def __init__(self, work_space, id, name='test', description='test', verbose=False):
        self.work_space = work_space
        self.skil = self.work_space.skil
        self.id = id

        add_experiment_response = self.skil.api.add_experiment(
            self.skil.server_id,
            skil_client.ExperimentEntity(
                experiment_id=id,
                experiment_name=name,
                experiment_description=description,
                model_history_id=self.work_space.history_id
            )
        )
        if verbose:
            self.skil.printer.pprint(add_experiment_response)
