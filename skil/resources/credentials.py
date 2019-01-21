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
        create   
    """

    def __init__(self, skil, cred_type, uri, name=None, create=True, *args, **kwargs):
        self.skil = skil
        if not cred_type in ["AWS", "Azure", "GoogleCloud", "Hadoop"]:
            raise ValueError("cred_type {} not supported".format(cred_type))
        self.cred_type = cred_type
        self.uri = uri
        self.name = name

        if create:
            request_body = AddCredentialsRequest(
                type=self.cred_type, name=self.name, uri=self.uri)
            response = self.skil.api.add_credentials(request_body)
            self.id = response.credential_id

    def delete(self):
        """Delete these credentials from SKIL.
        """
        if self.id:
            self.skil.api.delete_credentials_by_id(self.id)
            self.id = None


def AWS(Credentials):
    def __init__(self, skil, uri, name=None):
        super(AWS, self).__init__(
            skil=skil, cred_type="AWS", uri=uri, name=name)


def Azure(Credentials):
    def __init__(self, skil, uri, name=None):
        super(Azure, self).__init__(
            skil=skil, cred_type="Azure", uri=uri, name=name)


def GoogleCloud(Credentials):
    def __init__(self, skil, uri, name=None):
        super(GoogleCloud, self).__init__(
            skil=skil, cred_type="GoogleCloud", uri=uri, name=name)


def Hadoop(Credentials):
    def __init__(self, skil, uri, name=None):
        super(Hadoop, self).__init__(
            skil=skil, cred_type="Hadoop", uri=uri, name=name)


def delete_credentials_by_id(skil, credentials_id):
    try:
        resp = skil.api.delete_credentials_by_id(credentials_id)
    except:
        raise Exception(
            'Credentials with id {} could not be deleted, make sure they exist.'.format(credentials_id))


def get_credentials_by_id(skil, credentials_id):
    response = skil.api.get_credentials_by_id(credentials_id)
    cred = Credentials(skil=skil, cred_type=response.type, uri=response.uri,
                       name=response.name, create=False)
    cred.id = credentials_id
    return cred
