import skil_client


class Experiment:

    def __init__(self, work_space, id=None, name='test', description='test', verbose=False):
        self.work_space = work_space
        self.skil = self.work_space.skil
        self.id = id if id else work_space.id + "_experiment"

        add_experiment_response = self.skil.api.add_experiment(
            self.skil.server_id,
            skil_client.ExperimentEntity(
                experiment_id=self.id,
                experiment_name=name,
                experiment_description=description,
                model_history_id=self.work_space.id
            )
        )
        if verbose:
            self.skil.printer.pprint(add_experiment_response)

    def delete(self):
        try:
            api_response = self.skil.api.delete_experiment(
                self.work_space.id, self.id)
            self.skil.printer.pprint(api_response)
        except skil_client.rest.ApiException as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_experiment: %s\n" % e)


# TODO: define "get_experiment_by_id"