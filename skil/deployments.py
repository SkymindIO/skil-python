import skil_client


class Deployment:

    def __init__(self, skil, name=None, id=None):
        if id is not None:
            response = skil.api.deployment_get(id)
            if response is None:
                raise KeyError('Deployment not found: ' + str(id))
            self.response = response
        else:
            self.name = name if name else 'deployment'
            create_deployment_request = skil_client.CreateDeploymentRequest(self.name)
            self.response = skil.api.deployment_create(create_deployment_request)


def get_deployement_by_id(skil, id):
    dep = Deployment(skil, id=id)
    return dep
