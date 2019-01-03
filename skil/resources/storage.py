import skil_client


class StorageResource:
    """StorageResource

    A SKIL storage resource is an abstraction for (cloud and on-premise)
    storage capabilities, including systems like AWS S3,
    HDFS, Azure Storage or Google Cloud storage.
    """
    __metaclass__ = type

    def __init__(self, skil):
        """Adds the storage resource to SKIL.
        """
        self.skil = skil
        self.resource_id = None

    def delete(self):
        """Delete the storage resource from SKIL.
        """
        if self.resource_id:
            self.skil.api.delete_resource_by_id(resource_id=self.resource_id)


class AzureStorage(StorageResource):
    """AzureStorage

    SKIL Azure storage resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        container_name: Azure storage container name
    """

    def __init__(self, skil, name, container_name, credential_uri):
        super(AzureStorage, self).__init__(skil)

        self.name = name
        self.container_name = container_name
        self.credential_uri = credential_uri

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.AzureStorageResourceDetails(
                container_name=self.container_name
            ),
            credential_uri=self.credential_uri,
            type="STORAGE",
            sub_type="AzureStorage")
        )

        self.resource_id = resource_response.get("resourceId")


class GoogleStorage(StorageResource):
    """GoogleStorage

    SKIL Google storage resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        project_id: Google project ID
        bucket_name: bucket name
    """

    def __init__(self, skil, name, project_id, bucket_name, credential_uri):

        super(GoogleStorage, self).__init__(skil)
        self.name = name
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.credential_uri = credential_uri

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.GoogleStorageResourceDetails(
                project_id=self.project_id,
                bucket_name=self.bucket_name
            ),
            credential_uri=self.credential_uri,
            type="STORAGE",
            sub_type="GoogleStorage")
        )

        self.resource_id = resource_response.get("resourceId")


class HDFS(StorageResource):
    """HDFS

    SKIL HDFS resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        name_node_host: host of the name node
        name_node_port: port of the name node
    """

    def __init__(self, skil, name, name_node_host, name_node_port, credential_uri):

        super(HDFS, self).__init__(skil)
        self.name = name
        self.name_node_host = name_node_host
        self.name_node_port = name_node_port
        self.credential_uri = credential_uri

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.HDFSResourceDetails(
                name_node_host=self.name_node_host,
                name_node_port=self.name_node_port
            ),
            credential_uri=self.credential_uri,
            type="STORAGE",
            sub_type="HDFS")
        )

        self.resource_id = resource_response.get("resourceId")


class S3(StorageResource):
    """S3

    SKIL S3 resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        bucket: S3 bucket name
        region: AWS region
    """

    def __init__(self, skil, name, bucket, region, credential_uri):

        super(S3, self).__init__(skil)
        self.name = name
        self.bucket = bucket
        self.region = region
        self.credential_uri = credential_uri

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.S3ResourceDetails(
                bucket=self.bucket,
                region=self.region
            ),
            credential_uri=self.credential_uri,
            type="STORAGE",
            sub_type="S3")
        )

        self.resource_id = resource_response.get("resourceId")

# TODO: get resource from ID
