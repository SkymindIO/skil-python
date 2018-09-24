import skil_client


class WorkSpace:

    def __init__(self, skil, name=None, labels=None, verbose=False):
        self.skil = skil
        self.printer = self.skil.printer
        self.name = name if name else 'skil_workspace'

        self.workspace = self.skil.api.add_model_history(
            self.skil.server_id,
            skil_client.AddModelHistoryRequest(name, labels)
        )
        self.id = self.workspace.model_history_id

        if verbose:
            self.printer.pprint(self.workspace)
