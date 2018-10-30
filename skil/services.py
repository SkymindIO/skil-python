import skil_client
import time
import uuid
import numpy as np

class Service:

    def __init__(self, skil, model_name, deployment, model_deployment):
        self.skil = skil
        self.model_name = model_name
        self.model_deployment = model_deployment
        self.deployment = deployment

    def start(self):
        if not self.model_deployment:
            self.skil.printer.pprint(
                "No model deployed yet, call 'deploy()' on a model first.")
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
                    self.skil.printer.pprint(
                        ">>> Model server started successfully!")
                    break
                else:
                    self.skil.printer.pprint(">>> Waiting for deployment...")

    def stop(self):
        # TODO: test this
        self.skil.api.model_state_change(
            self.deployment.id,
            self.model_deployment.id,
            skil_client.SetState("stop")
        )

    def indarray(self, np_array):
        return skil_client.INDArray(
            ordering='c',
            shape=list(np_array.shape),
            data = np_array.tolist()
        )

    def predict(self, data):
        inputs = [self.indarray(x) for x in data]

        # This is the keep_prob placeholder data
        inputs.append(self.indarray(np.array([1.0])))

        classification_response = self.skil.api.multipredict(
            deployment_name=self.deployment.name,
            model_name=self.model_name,
            version_name="default",
            body=skil_client.MultiPredictRequest(
                id=str(uuid.uuid1()),
                needs_pre_processing=False,
                inputs=inputs
            )
        )
        outputs = classification_response.outputs
        outputs = [np.asarray(o.data).reshape(o.shape) for o in outputs]
        if len(outputs) == 1:
            return outputs[0]
        return outputs

    def predict_single(self, data):
        inputs = [self.indarray(data.expand_dims(0))]

        # This is the keep_prob placeholder data
        inputs.append(self.indarray(np.array([1.0])))

        classification_response = self.skil.api.multipredict(
            deployment_name=self.deployment.name,
            model_name=self.model_name,
            version_name="default",
            body=skil_client.MultiPredictRequest(
                id=str(uuid.uuid1()),
                needs_pre_processing=False,
                inputs=inputs
            )
        )
        output = classification_response[0]
        return np.asarray(output.data).reshape(output.shape)
