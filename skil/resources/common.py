from .base import Resource
from .compute import *
from .storage import *


def get_all_resources(skil):
    '''Get all current SKIL resources as a list of
    skil.resources.base.Resource instances.
    '''
    raise NotImplementedError


def get_resource_by_id(skil, resource_id):
    '''Get a skil.resources.base.Resource object
    by ID.
    '''
    # TODO test this
    api_response = skil.api.get_resource_by_id(resource_id)
    return Resource(skil, api_response.resource_id)


def get_resources_by_type(skil, type):
    '''Get a list of skil.resources.base.Resource objects
    by type ('compute' or 'storage').
    '''
    raise NotImplementedError


def get_resources_by_sub_type(skil, sub_type):
    '''Get a list of resources by string sub_type, namely 
        - EMR                   # AWS Elastic Map Reduce(Compute)
        - S3                    # AWS Simple Storage Service
        - GoogleStorage         # Google Cloud Storage
        - DataProc              # Google Big Data Compute Engine
        - HDInsight             # Azure Compute
        - AzureStorage          # Azure Blob Storage
        - HDFS                  # in house Hadoop (Storage)

    For instance, choosing 'EMR' sub_type, you'll get all
    skil.resources.compute.EMR resource instances in a Python list.
    '''
    # TODO: use "get_resource_details_by_id" here and just return the list.
    raise NotImplementedError


def get_resource_details_by_id(skil, resource_id):
    '''Get a concrete resource implementation of
    skil.resources.base.Resource by resource ID. For instance, if
    your resource ID corresponds to a resource of subtype "HDFS",
    this will return a skil.resources.storage.HDFS object.
    '''
    resource = skil.api.get_resource_by_id(resource_id)
    res_type = resource.type

    details = skil.api.get_resource_details_by_id(resource_id)
    # TODO: we get the credentials ID (not the URI) from "resource",
    #   in "details" there's nothing. So we set "credential_uri" to None for lack of a better idea.
    if res_type == 'EMR':
        return EMR(skil, details.name, details.region, None,
                   details.clusterId, resource_id, False)
    elif res_type == 'S3':
        return S3(skil, details.name, details.bucket, details.region, None, resource_id, False)
    else:
        # TODO complete this
        pass
