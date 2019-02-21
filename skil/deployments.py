import skil_client
from .base import Skil
import uuid
import json


class Deployment:
    """Deployments operate independently of workspaces to ensure that there are
    no accidental interruptions or mistakes in a production environment.

    # Arguments:
        skil: `Skil` server instance.
        name: string. Name for the deployment.
        id: Unique id for the deployment. If `None`, a unique id will be generated.
    """
    # TODO: starting from skil 1.2 deployments are linked to workspaces and experiments.
    # Make sure to keep this up-to-date.

    def __init__(self, skil=None, name=None, deployment_id=None):
        if not skil:
            skil = Skil()  # TODO: take care of auth
        if deployment_id is not None:
            response = skil.api.deployment_get(deployment_id)
            if response is None:
                raise KeyError('Deployment not found: ' + str(deployment_id))
            self.response = response
            self.name = self.response.name
            self.id = deployment_id
        else:
            self.name = name if name else 'deployment-' + str(uuid.uuid1())[:8]
            create_deployment_request = skil_client.CreateDeploymentRequest(
                self.name)
            self.response = skil.api.deployment_create(
                create_deployment_request)
            self.id = self.response.id
        self.skil = skil

    def get_config(self):
        return {
            'deployment_id': self.id
        }

    def save(self, file_name):
        config = self.get_config()
        with open(file_name, 'w') as f:
            json.dump(config, f)

    @classmethod
    def load(cls, file_name):
        with open(file_name, 'r') as f:
            config = json.load(f)
        skil = Skil.from_config()
        return get_deployment_by_id(skil, config['deployment_id'])


def get_deployment_by_id(skil, deployment_id):
    """ Get model deployment by ID

    # Arguments
        skil: `Skil` server instance
        deployment_id: deployment ID
    """
    return Deployment(skil=skil, deployment_id=deployment_id)
