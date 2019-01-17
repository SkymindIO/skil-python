from .base import Resource
from .compute import *
from .storage import *


'''Get all current SKIL resources as a list of
skil.resources.base.Resource instances.
'''
def get_all_resources(skil):
    raise NotImplementedError


'''Get a skil.resources.base.Resource object
by ID.
'''
def get_resource_by_id(skil, resource_id):
    raise NotImplementedError


'''Get a list of skil.resources.base.Resource objects
by type ('compute' or 'storage').
'''
def get_resources_by_type(skil, type):
    raise NotImplementedError


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
def get_resources_by_sub_type(skil, sub_type):
    raise NotImplementedError


'''Get a concrete resource implementation of
skil.resources.base.Resource by ID. For instance, if
your resource ID corresponds to a resource of subtype "HDFS",
this will return a skil.resources.storage.HDFS object.

'''
def get_resource_details_by_id(skil, resource_id):
    raise NotImplementedError
