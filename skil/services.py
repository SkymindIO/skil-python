import skil_client
import time
import uuid
import numpy as np

class Service:
    '''A wrapper around a deployed model for inference.
    '''
    def __init__(self, skil, model_name, deployment, model_deployment):
        self.skil = skil
        self.model_name = model_name
        self.model_deployment = model_deployment
        self.deployment = deployment

    def start(self):
        '''Starts the service.
        '''
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
                    time.sleep(15)
                    self.skil.printer.pprint(
                        ">>> Model server started successfully!")
                    break
                else:
                    self.skil.printer.pprint(">>> Waiting for deployment...")


    def stop(self):
        '''Stop the service.
        '''
        # TODO: test this
        self.skil.api.model_state_change(
            self.deployment.id,
            self.model_deployment.id,
            skil_client.SetState("stop")
        )

    def _indarray(self, np_array):
        '''Convert a numpy array to `skil_client.INDArray` instance.

        # Arguments
        np_array: `numpy.ndarray` instance.

        # Returns
        `skil_client.INDArray` instance.
        '''
        return skil_client.INDArray(
            ordering='c',
            shape=list(np_array.shape),
            data = np_array.tolist()
        )

    def predict(self, data):
        '''Predict for given batch of data.

        # Argments
        data: `numpy.ndarray` (or list thereof). Batch of input data, or list of batches for multi-input model.

        # Returns
        `numpy.ndarray` instance for single output model and list of `numpy.ndarray` for multi-ouput model.
        '''
        if isinstance(data, list):
            inputs = [self._indarray(x) for x in data]
        else:
            inputs = [self._indarray(data)]

        # This is the keep_prob placeholder data
        inputs.append(self._indarray(np.array([1.0])))

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
        '''Predict for a single input.

        # Argments
        data: `numpy.ndarray` (or list thereof). Input data.

        # Returns
        `numpy.ndarray` instance for single output model and list of `numpy.ndarray` for multi-ouput model.
        '''
        inputs = [self._indarray(data.expand_dims(0))]

        # This is the keep_prob placeholder data
        inputs.append(self._indarray(np.array([1.0])))

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
