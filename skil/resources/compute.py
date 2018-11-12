import abc
import skil_client

class ComputeResource:
    """ComputeResource

    A SKIL compute resource is an abstraction for (cloud)
    compute capabilities, including systems like AWS EMR
    and GCE DataProc.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Adds the compute resource to SKIL.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self):
        """Delete the compute resource from SKIL.
        """
        raise NotImplementedError


class EMRResource(ComputeResource):

    def __init__(self, skil, name, region, credential_uri, cluster_id=None):
        self.skil = skil
        self.name = name
        self.region = region
        # TODO: can we hide setting credentials? i.e. can these be put into a
        # little config file (similar to what we do in pydl4j?). this is tedious
        # for users
        self.credential_uri = credential_uri

        # TODO: if cluster_id is None, spin up a cluster and retrieve id (requires work in SKIL core)
        self.cluster_id = cluster_id

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.EMRResourceDetails(
                cluster_id=self.cluster_id, 
                region=self.region
            ),
            credential_uri=self.credential_uri,
            type="COMPUTE",
            sub_type="EMR")
        )

        self.resource_id = resource_response.get("resourceId")
    
    def delete(self):
        self.skil.api.delete_resource_by_id(resource_id=self.resource_id)


class DataProcResourceDetails(ComputeResource):

    def __init__(self, skil, name, project_id, region, spark_cluster_name):
        self.skil = skil
        self.name = name
        self.project_id = project_id
        self.region = region
        self.cluster_name = spark_cluster_name

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.DataProcResourceDetails(
                project_id=self.project_id, 
                region=self.region,
                spark_cluster_name=self.cluster_name
            ),
            type="COMPUTE",
            sub_type="DataProc")
        )

        self.resource_id = resource_response.get("resourceId")
    
    def delete(self):
        self.skil.api.delete_resource_by_id(resource_id=self.resource_id)