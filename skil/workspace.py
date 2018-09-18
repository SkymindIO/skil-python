import skil_client


class WorkSpace():

    def __init__(self, skil, name='jupyter_ws', labels='jupyter, python', verbose=False):
        self.skil = skil
        self.printer = self.skil.printer

        self.model_history = self.skil.api.add_model_history(
            self.skil.server_id,
            skil_client.AddModelHistoryRequest(name, labels)
        )
        self.history_id = self.model_history.model_history_id

        if verbose:
            self.printer.pprint(self.model_history)
