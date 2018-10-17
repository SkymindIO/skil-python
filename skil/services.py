import skil_client
import time
import uuid


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

    def predict(self, data):
        # TODO: this evaluates a single example, i.e. mini-batch of one.
        # generalize this to general case.
        classification_response = self.skil.api.multipredict(
            deployment_name=self.deployment.name,
            model_name=self.model_name,
            version_name="default",
            body=skil_client.MultiPredictRequest(
                id=str(uuid.uuid1()),
                needs_pre_processing=False,
                inputs=[
                    skil_client.INDArray(
                        ordering='c',
                        shape=list(data.shape),
                        data=data.tolist()
                    ),
                    skil_client.INDArray(  # This is the keep_prob placeholder data
                        ordering='c',
                        shape=[1],
                        data=[1.0]
                    )
                ]
            )
        )
        output = classification_response.get('outputs')[0]
        prediction = output.get('data')
        shape = output.get('shape')
        return prediction.reshape(shape)