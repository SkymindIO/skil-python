import skil_client


class Experiment:

    def __init__(self, work_space=None, id=None, name='test', description='test', verbose=False, create=True):
        if create:
            self.work_space = work_space
            self.skil = self.work_space.skil
            self.id = id if id else work_space.id + "_experiment"

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

    def delete(self):
        try:
            api_response = self.skil.api.delete_experiment(
                self.work_space.id, self.id)
            self.skil.printer.pprint(api_response)
        except skil_client.rest.ApiException as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_experiment: %s\n" % e)

def get_experiment_by_id(work_space, id):
    return Experiment(work_space=work_space, id=id, create=False)
