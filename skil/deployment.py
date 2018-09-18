import skil_client
import pprint
import os
import time


class Deployment():

    def __init__(self, skil, name):
        self.name = name
        create_deployment_request = skil_client.CreateDeploymentRequest(name)
        self.response = skil.api.deployment_create(create_deployment_request)
