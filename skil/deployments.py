import skil_client


class Deployment:

    def __init__(self, skil, name=None):
        self.name = name if name else 'deployment'
        create_deployment_request = skil_client.CreateDeploymentRequest(self.name)
        self.response = skil.api.deployment_create(create_deployment_request)
