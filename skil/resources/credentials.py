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
    def __init__(self, skil, cred_type, uri, name=None, create=True, *args, **kwargs):
        self.skil = skil
        if not cred_type in ["AWS", "Azure", "GoogleCloud", "Hadoop"]:
            raise ValueError("cred_type {} not supported".format(cred_type))
        self.cred_type = cred_type
        self.uri = uri
        self.name = name

        if create:
            request_body = AddCredentialsRequest(type=self.cred_type, name=self.name, uri=self.uri)
            response = self.skil.api.add_credentials(request_body)
            self.id = response.credential_id

    def delete(self):
        """Delete these credentials from SKIL.
        """
        if self.id:
            self.skil.api.delete_credentials_by_id(self.id)


def delete_credentials_by_id(skil, credentials_id):
    skil.api.delete_credentials_by_id(credentials_id)


def get_credentials_by_id(skil, credentials_id):
    response = skil.api.get_credentials_by_id(credentials_id)
    cred = Credentials(skil=skil, cred_type=response.type, uri=response.uri, 
                       name=response.name, create=False)
    cred.id = credentials_id
    return cred