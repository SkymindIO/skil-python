import skil_client
import time


class Model():
    def __init__(self, experiment, model_path, id, name, version,
                 labels='', verbose=False):
        self.experiment = experiment
        self.work_space = experiment.work_space
        self.skil = self.work_space.skil
        self.model_path = model_path
        self.id = id
        self.name = name
        self.evaluations = {}

        add_model_instance_response = self.skil.api.add_model_instance(
            self.skil.server_id,
            skil_client.ModelInstanceEntity(
                uri=model_path,
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

    def deploy(self, deployment, input_names=["input_node", "keep_prob_input"],
               output_names=["output_node"]):   
        
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

        model_deployment_response = self.skil.api.deploy_model(deployment.response.id, deploy_model_request)
        self.skil.printer.pprint(model_deployment_response)