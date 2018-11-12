import skil_client

class StorageResource:
    """StorageResource

    A SKIL storage resource is an abstraction for (cloud)
    storage capabilities, including systems like AWS S3,
    HDFS, Azure Storage or Google Cloud storage.
    """
    def __init__(self):
        """Adds the storage resource to SKIL.
        """
        pass

    def delete(self):
        """Delete the storage resource from SKIL.
        """
        self.skil.api.delete_resource_by_id(resource_id=self.resource_id)


class AzureStorage(StorageResource):

    def __init__(self, skil, name, container_name):

        self.skil = skil
        self.name = name
        self.container_name = container_name

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.AzureStorageResourceDetails(
                container_name = self.container_name
            ),
            type="STORAGE",
            sub_type="AzureStorage")
        )

        self.resource_id = resource_response.get("resourceId")
    

class GoogleStorage(StorageResource):

    def __init__(self, skil, name, project_id, bucket_name):

        self.skil = skil
        self.name = name
        self.project_id = project_id
        self.bucket_name = bucket_name

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.GoogleStorageResourceDetails(
                project_id = self.project_id,
                bucket_name = self.bucket_name
            ),
            type="STORAGE",
            sub_type="GoogleStorage")
        )

        self.resource_id = resource_response.get("resourceId")


class HDFS(StorageResource):

    def __init__(self, skil, name, name_node_host, name_node_port):

        self.skil = skil
        self.name = name
        self.name_node_host = name_node_host
        self.name_node_port = name_node_port

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.HDFSResourceDetails(
                name_node_host = self.name_node_host,
                name_node_port = self.name_node_port
            ),
            type="STORAGE",
            sub_type="HDFS")
        )

        self.resource_id = resource_response.get("resourceId")


class S3(StorageResource):

    def __init__(self, skil, name, bucket, region):

        self.skil = skil
        self.name = name
        self.bucket = bucket
        self.region = region

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.S3ResourceDetails(
                bucket = self.bucket,
                region = self.region
            ),
            type="STORAGE",
            sub_type="S3")
        )

        self.resource_id = resource_response.get("resourceId")