from skil_client import AddCredentialsRequest
import skil_client

class Credentials:
    """Credentials

    SKIL resource credentials manage cloud provider and other credentials for you.
    Currently supported credentials are AWS, Azure, GoogleCloud and Hadoop

    # Arguments:
        skil: `Skil` server instance
        cred_type: credentials type string, either "AWS", "Azure", GoogleCloud" or "Hadoop"
        uri: URI pointing to the credentials
        name: Name of the resource    
    """

    def __init__(self, skil, cred_type, uri, name=None, *args, **kwargs):
        """Add the resource to SKIL.
        """
        self.skil = skil
        if not cred_type in list("AWS", "Azure", "GoogleCloud", "Hadoop"):
            raise ValueError("cred_type {} not supported".format(cred_type))
        self.cred_type = cred_type
        self.uri = uri
        self.name = name

        request_body = AddCredentialsRequest(type=self.cred_type, name=self.name, uri=self.uri)
        response = self.skil.api.add_credentials(request_body)

    def delete(self):
        """Delete the resource from SKIL.
        """
        if self.resource_id:
            self.skil.api.delete_resource_by_id(resource_id=self.resource_id)
