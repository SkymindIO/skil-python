import skil
import skil_client
import time
import os


class Model:
    def __init__(self, model_file_name, id=None, name=None, version=None, experiment=None,
                 labels='', verbose=False):

        if not experiment:
            self.skil = skil.Skil()
            self.work_space = skil.workspace.WorkSpace(self.skil)
            self.experiment = skil.experiment.Experiment(self.work_space)
        else:
            self.experiment = experiment
            self.work_space = experiment.work_space
            self.skil = self.work_space.skil
        self.skil.upload_model(os.path.join(os.getcwd(), model_file_name))

        self.model_name = model_file_name
        self.model_path = self.skil.get_model_path(model_file_name)
        self.id = id if id else model_file_name
        self.name = name if name else model_file_name
        self.version = version if version else 1

        self.evaluations = {}

        add_model_instance_response = self.skil.api.add_model_instance(
            self.skil.server_id,
            skil_client.ModelInstanceEntity(
                uri=self.model_path,
                model_id=id,
                model_labels=labels,
                model_name=name,
                model_version=self.version,
                created=int(round(time.time() * 1000)),
                experiment_id=self.experiment.id
            )
        )
        if verbose:
            self.skil.printer.pprint(add_model_instance_response)

    def delete(self):
        try:
            self.skil.api.delete_model_instance(self.skil.server_id, self.id)
        except skil_client.rest.ApiException as e:
            self.skil.printer.pprint(">>> Exception when calling delete_model_instance: %s\n" % e)

    def add_evaluation(self, accuracy,  id=None, name=None, version=None):

        eval_version = version if version else 1
        eval_id = id if id else self.id
        eval_name = name if name else self.id

        eval_response = self.skil.api.add_evaluation_result(
            self.skil.server_id,
            skil_client.EvaluationResultsEntity(
                evaluation="",  # TODO: what is this?
                created=int(round(time.time() * 1000)),
                eval_name=eval_name,
                model_instance_id=self.id,
                accuracy=float(accuracy),
                eval_id=eval_id,
                eval_version=eval_version
            )
        )
        self.evaluations[id] = eval_response

    def deploy(self, deployment=None, input_names=None,
               output_names=None, verbose=True):

        if not deployment:
            deployment = skil.Deployment(self.skil)

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
            self.deployment.id, deploy_model_request)
        if verbose:
            self.skil.printer.pprint(self.model_deployment)

    def undeploy(self):
        try:
            self.skil.api.delete_model(self.deployment.id, self.id)
        except skil_client.rest.ApiException as e:
            self.skil.printer.pprint(">>> Exception when calling delete_model_instance: %s\n" % e)

    def serve(self):
        if not self.model_deployment:
            self.skil.printer.pprint("No model deployed yet, call 'deploy()' on a model first.")
        else:
            self.skil.api.model_state_change(
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
                    self.skil.printer.pprint(">>> Model server started successfully!")
                    break
                else:
                    self.skil.printer.pprint(">>> Waiting for deployment...")
