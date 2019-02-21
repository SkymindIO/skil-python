from .base import Resource
from .compute import *
from .storage import *


def get_all_resources(skil):
    '''Get all current SKIL resources as a list of
    skil.resources.base.Resource instances.
    '''
    resource_list = skil.api.get_resources()
    resources = []

    for resource_obj in resource_list:
        resource = Resource(skil)
        resource.resource_id = resource_obj.resource_id
        resources.append(resource)
    return resources


def get_resource_by_id(skil, resource_id):
    '''Get a skil.resources.base.Resource object
    by ID.
    '''
    api_response = skil.api.get_resource_by_id(resource_id)
    return Resource(skil, api_response.resource_id)


def get_resources_by_type(skil, resource_type):
    '''Get a list of skil.resources.base.Resource objects
    by type ('compute' or 'storage').
    '''
    resource_list = skil.api.get_resource_by_type(resource_type)
    resource_ids = [resource.resource_id for resource in resource_list]
    return [get_resource_by_id(skil, resource_id)
            for resource_id in resource_ids]


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
    subtype_list = skil.api.get_resource_by_sub_type(sub_type)
    return [get_resource_details_by_id(
        skil, obj.resource_id) for obj in subtype_list]


def get_resource_details_by_id(skil, resource_id):
    '''Get a concrete resource implementation of
    skil.resources.base.Resource by resource ID. For instance, if
    your resource ID corresponds to a resource of subtype "HDFS",
    this will return a skil.resources.storage.HDFS object.
    '''
    resource = skil.api.get_resource_by_id(resource_id)
    res_type = resource.sub_type

    details = skil.api.get_resource_details_by_id(resource_id)
    if res_type == 'EMR':
        return EMR(skil, resource.name, details['region'], None,
                   details['clusterId'], resource_id, False)
    elif res_type == 'S3':
        return S3(skil, resource.name,
                  details['bucket'], details['region'], None, resource_id, False)
    elif res_type == 'GoogleStorage':
        return GoogleStorage(
            skil, resource.name, details['projectId'], details['bucketName'], None, resource_id, False)
    elif res_type == 'DataProc':
        return DataProc(skil, resource.name, details['projectId'], details['region'],
                        details['sparkClusterName'], None, resource_id, False)
    elif res_type == 'HDInsight':
        return HDInsight(skil, resource.name, details['subscriptionId'], details['resourceGroupName'],
                         details['clusterName'], None, resource_id, False)
    elif res_type == 'AzureStorage':
        return AzureStorage(
            skil, resource.name, details['containerName'], None, resource_id, False)
    elif res_type == 'HDFS':
        return HDFS(skil, resource.name, details['nameNodeHost'],
                    details['nameNodePort'], None, resource_id, False)
    elif res_type == 'YARN':
        return YARN(skil, resource.name,
                    details['localSparkHome'], None, resource_id, False)
