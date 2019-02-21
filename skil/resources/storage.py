import skil_client
from .base import Resource


class AzureStorage(Resource):
    """AzureStorage

    SKIL Azure storage resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        container_name: Azure storage container name
        credential_uri: path to credential file
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """

    def __init__(self, skil, name, container_name, credential_uri,
                 resource_id=None, create=True):

        super(AzureStorage, self).__init__(skil)

        self.name = name
        self.container_name = container_name
        self.credential_uri = credential_uri
        self.resource_id = resource_id

        if create:
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
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')


class GoogleStorage(Resource):
    """GoogleStorage

    SKIL Google storage resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        project_id: Google project ID
        bucket_name: bucket name
        credential_uri: path to credential file
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """

    def __init__(self, skil, name, project_id, bucket_name, credential_uri,
                 resource_id=None, create=True):

        super(GoogleStorage, self).__init__(skil)
        self.name = name
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.credential_uri = credential_uri
        self.resource_id = resource_id

        if create:
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
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')


class HDFS(Resource):
    """HDFS

    SKIL HDFS resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        name_node_host: host of the name node
        name_node_port: port of the name node
        credential_uri: path to credential file
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """

    def __init__(self, skil, name, name_node_host, name_node_port, credential_uri,
                 resource_id=None, create=True):

        super(HDFS, self).__init__(skil)
        self.name = name
        self.name_node_host = name_node_host
        self.name_node_port = name_node_port
        self.credential_uri = credential_uri
        self.resource_id = resource_id

        if create:
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
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')


class S3(Resource):
    """S3

    SKIL S3 resource.

    # Arguments:
        skil: `Skil` server instance
        name: Resource name
        bucket: S3 bucket name
        region: AWS region
        credential_uri: path to credential file
        resource_id: optional resource ID to retrieve an existing resource
        create: boolean, for internal use only. whether to create a new resource or not
    """

    def __init__(self, skil, name, bucket, region, credential_uri,
                 resource_id=None, create=True):

        super(S3, self).__init__(skil)
        self.name = name
        self.bucket = bucket
        self.region = region
        self.credential_uri = credential_uri
        self.resource_id = resource_id

        if create:
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
        else:
            if resource_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid resource_id')
