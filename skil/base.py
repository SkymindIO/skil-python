import skil_client
import pprint
import os
import time
import requests
import json
import subprocess


def start_skil_docker():
    devnull = open(os.devnull, 'w')

    print(">>> Downloading latest SKIL docker image.")
    subprocess.call(["docker", "pull", "skymindops/skil-ce"])
    print(">>> Starting SKIL docker container.")
    subprocess.Popen(["docker", "run", "--rm", "-it", "-p", "9008:9008",
                      "-p", "8080:8080", "skymindops/skil-ce", "bash", "/start-skil.sh", "&"],
                     stdout=devnull, stderr=subprocess.STDOUT)
    print("Starting SKIL. This process will take a few seconds to start.")
    time.sleep(20)
    print("SKIL started! Visit http://localhost:9008 to work with the UI.")


class Skil:
    def __init__(self, workspace_server_id=None, host='localhost', port=9008,
                 debug=False, user_id='admin', password='admin'):

        self.printer = pprint.PrettyPrinter(indent=4)

        config = skil_client.Configuration()
        config.host = "{}:{}".format(host, port)
        config.debug = debug
        self.config = config
        self.uploads = []
        self.uploaded_model_names = []
        self.auth_headers = None

        self.api_client = skil_client.ApiClient(configuration=config)
        self.api = skil_client.DefaultApi(api_client=self.api_client)

        try:
            self.printer.pprint('>>> Authenticating SKIL...')
            credentials = skil_client.Credentials(
                user_id=user_id, password=password)
            token = self.api.login(credentials)
            self.token = token.token
            config.api_key['authorization'] = self.token
            config.api_key_prefix['authorization'] = "Bearer"
            self.printer.pprint('>>> Done!')
        except skil_client.rest.ApiException as e:
            raise Exception(
                "Exception when calling DefaultApi->login: {}\n".format(e))

        if workspace_server_id:
            self.server_id = workspace_server_id
        else:
            self.server_id = self.get_default_server_id()

    def get_default_server_id(self):
        self.auth_headers = {'Authorization': 'Bearer %s' % self.token}
        r = requests.get(
            'http://{}/services'.format(self.config.host), headers=self.auth_headers)
        if r.status_code != 200:
            r.raise_for_status()

        content = json.loads(r.content.decode('utf-8'))
        services = content.get('serviceInfoList')
        for s in services:
            if 'Model History' in s.get('name'):
                id = s.get('id')
        if id:
            return id
        else:
            raise Exception(
                "Could not detect default model history server instance. Is SKIL running?")

    def upload_model(self, model_name):
        self.printer.pprint('>>> Uploading model, this might take a while...')
        upload = self.api.upload(file=model_name).file_upload_response_list
        self.uploads = self.uploads + upload
        self.uploaded_model_names.append(model_name)
        self.printer.pprint(self.uploads)

    def get_uploaded_model_names(self):
        return self.uploaded_model_names

    def get_model_path(self, model_name):
        for upload in self.uploads:
            if model_name == upload.file_name:
                return "file://" + upload.path
        raise Exception("Model resource not found, did you upload it? ")
