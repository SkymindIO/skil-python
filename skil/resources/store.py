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


class AzureStorageResourceDetails(StorageResource):

    def __init__(self, skil, name, container_name):

        self.skil = skil
        self.name = name
        self.container_name = container_name

        resource_response = self.skil.api.add_resource(skil_client.AddResourceRequest(
            resource_name=self.name,
            resource_details=skil_client.DataProcResourceDetails(
                container_name = self.container_name
            ),
            type="STORAGE",
            sub_type="AzureStorage")
        )

        self.resource_id = resource_response.get("resourceId")
    
