import skil_client
import time
import os

class Model():
    def __init__(self, experiment, model_name, id, name, version,
                 labels='', verbose=False):

        self.experiment = experiment
        self.work_space = experiment.work_space
        self.skil = self.work_space.skil
        self.skil.upload_model(os.path.join(os.getcwd(), model_name))

        self.model_name = model_name
        self.model_path = self.skil.get_model_path(model_name)
        self.id = id
        self.name = name
        self.evaluations = {}

        add_model_instance_response = self.skil.api.add_model_instance(
            self.skil.server_id,
            skil_client.ModelInstanceEntity(
                uri=self.model_path,
                model_id=id,
                model_labels=labels,
                model_name=name,
                model_version=version,
                created=int(round(time.time() * 1000)),
                experiment_id=self.experiment.id
            )
        )
        if verbose:
            self.skil.printer.pprint(add_model_instance_response)

    def add_evaluation(self, id, name, version, accuracy):

        eval_response = self.skil.api.add_evaluation_result(
            self.skil.server_id,
            skil_client.EvaluationResultsEntity(
                evaluation="",  # TODO: what is this?
                created=int(round(time.time() * 1000)),
                eval_name=name,
                model_instance_id=self.id,
                accuracy=float(accuracy),
                eval_id=id,
                eval_version=version
            )
        )
        self.evaluations[id] = eval_response

    def deploy(self, deployment, input_names=None,
               output_names=None, verbose=True):

        uris = ["{}/model/{}/default".format(deployment.name, self.name),
                "{}/model/{}/v1".format(deployment.name, self.name)]

        deploy_model_request = skil_client.ImportModelRequest(
            name=self.name,
            scale=1,
            file_location=self.model_path,
            model_type="model",
            uri=uris,
            input_names=input_names,
            output_names=output_names)

        self.deployment = deployment.response
        self.model_deployment = self.skil.api.deploy_model(
            deployment.response.id, deploy_model_request)
        if verbose:
            self.skil.printer.pprint(self.model_deployment)


    def serve(self):

        if not self.model_deployment:
            self.skil.printer.pprint("No model deployed yet, call 'deploy()' on a model first.")
        else:
            model_state_change_response = self.skil.api.model_state_change(
                self.deployment.id,
                self.model_deployment.id,
                skil_client.SetState("start")
            )

            self.skil.printer.pprint(">>> Starting to serve model...")
            while True:
                time.sleep(5)
                model_state = self.skil.api.model_state_change(
                    self.deployment.id,
                    self.model_deployment.id,
                    skil_client.SetState("start")
                ).state
                if model_state == "started":
                    time.sleep(2)
                    print(">>> Model server started successfully!")
                    break
                else:
                    print(">>> Waiting for deployment...")


