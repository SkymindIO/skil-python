import skil_client


class Deployment:
    """ Deployments operate independently of workspaces to ensure that there are no accidental interruptions or mistakes in a production environment.

    # Arguments:
    skil: Skil server instance.
    name: string. Name for the deployment.
    id: Unique id for the deployment. If `None`, a unique id will be generated.
    """
    def __init__(self, skil, name=None, id=None):
        if id is not None:
            response = skil.api.deployment_get(id)
            if response is None:
                raise KeyError('Deployment not found: ' + str(id))
            self.response = response
            self.name = self.response.name
        else:
            self.name = name if name else 'deployment'
            create_deployment_request = skil_client.CreateDeploymentRequest(self.name)
            self.response = skil.api.deployment_create(create_deployment_request)
            self.id = self.response.id


def get_deployement_by_id(skil, id):
    dep = Deployment(skil, id=id)
    return dep
