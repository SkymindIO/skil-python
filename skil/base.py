import skil_client
import pprint
import os
import time


class Skil():
    def __init__(self, model_server_id=None, host='localhost', port=9008,
                 debug=False, user_id='admin', password='admin'):

        self.printer = pprint.PrettyPrinter(indent=4)

        if model_server_id:
            self.server_id = model_server_id
        else:
            self.server_id = self.get_default_server_id()

        config = skil_client.Configuration()
        config.host = "{}:{}".format(host, port)
        config.debug = debug
        self.config = config

        self.api_client = skil_client.ApiClient(configuration=config)
        self.api = skil_client.DefaultApi(api_client=self.api_client)

        try:
            self.printer.pprint('>>> Authenticating with SKIL API...')
            credentials = skil_client.Credentials(
                user_id=user_id, password=password)
            token = self.api.login(credentials)
            self.printer.pprint(token)
            config.api_key['authorization'] = token.token
            config.api_key_prefix['authorization'] = "Bearer"
            self.printer.pprint('>>> Done!')
        except skil_client.rest.ApiException as e:
            raise Exception(
                "Exception when calling DefaultApi->login: {}\n".format(e))

    def get_default_server_id(self):
        pass  # TODO

    def upload_model(self, model_name):
        self.printer.pprint('>>> Uploading model, this might take a while...')
        self.uploads = self.api.upload(file=model_name)
        self.printer.pprint(self.uploads)

    def get_model_path(self, verbose=False):
        model_file_path = "file://" + \
            self.uploads.file_upload_response_list[0].path
        if verbose:
            self.printer.pprint(model_file_path)
        return model_file_path
