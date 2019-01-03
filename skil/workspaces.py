import skil_client
from skil_client.rest import ApiException as api_exception


class WorkSpace:
    """WorkSpace

    Workspaces are a collection of features that enable different tasks such as
    conducting experiments, training models, and test different dataset transforms.

    Workspaces are distinct from Deployments by operating as a space for 
    non-production work.

    # Arguments
        skil: Skil server instance
        name: string. Name for the workspace.
        labels: string. Labels associated with the workspace, useful for searching (comma seperated).
        verbose: boolean. If True, api response will be printed.
        create: boolean. Internal, do not use.
    """

    def __init__(self, skil=None, name=None, labels=None, verbose=False, create=True):
        if not create:
            return
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

    def delete(self):
        """Deletes the work space.
        """
        try:
            api_response = self.skil.api.delete_model_history(
                self.skil.server_id, self.id)
            self.skil.printer.pprint(api_response)
        except api_exception as e:
            self.skil.printer.pprint(
                ">>> Exception when calling delete_model_history: %s\n" % e)


def get_workspace_by_id(skil, workspace_id):
    """Get workspace by ID

    # Arguments:
        skil: `Skil` server instance
        workspace_id: string, workspace ID
    """
    server_id = skil.server_id
    response = skil.api.get_model_history(server_id, workspace_id)
    ws = WorkSpace(create=False)
    ws.skil = skil
    ws.printer = skil.printer
    ws.workspace = response
    ws.id = workspace_id
    ws.name = response.model_name
    return ws
