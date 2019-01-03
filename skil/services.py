import skil_client
import time
import uuid
import numpy as np
import requests
import json
import os

try:
    import cv2
except ImportError:
    cv2 = None


class Service:
    """Service

    A service is a deployed model.

    # Arguments:
        skil: `Skil` server instance
        model: `skil.Model` instance
        deployment: `skil.Deployment` instance
        model_deployment: result of `deploy_model` API call of a model
    """

    def __init__(self, skil, model, deployment, model_deployment):
        self.skil = skil
        self.model = model
        self.model_name = self.model.name
        self.model_deployment = model_deployment
        self.deployment = deployment

    def start(self):
        """Starts the service.
        """
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
        """Stops the service.
        """
        # TODO: test this
        self.skil.api.model_state_change(
            self.deployment.id,
            self.model_deployment.id,
            skil_client.SetState("stop")
        )

    @staticmethod
    def _indarray(np_array):
        """Convert a numpy array to `skil_client.INDArray` instance.

        # Arguments
            np_array: `numpy.ndarray` instance.

        # Returns
            `skil_client.INDArray` instance.
        """
        return skil_client.INDArray(
            ordering='c',
            shape=list(np_array.shape),
            data=np_array.reshape(-1).tolist()
        )

    def predict(self, data):
        """Predict for given batch of data.

        # Arguments:
            data: `numpy.ndarray` (or list thereof). Batch of input data, or list of batches for multi-input model.

        # Returns
            `numpy.ndarray` instance for single output model and list of `numpy.ndarray` for multi-output model.
        """
        if isinstance(data, list):
            inputs = [self._indarray(x) for x in data]
        else:
            inputs = [self._indarray(data)]

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
        """Predict for a single input.

        # Arguments:
            data: `numpy.ndarray` (or list thereof). Input data.

        # Returns
            `numpy.ndarray` instance for single output model and list of `numpy.ndarray` for multi-output model.
        """
        if isinstance(data, list):
            inputs = [self._indarray(np.expand_dims(x, 0)) for x in data]
        else:
            inputs = [self._indarray(np.expand_dims(data, 0))]

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
        output = classification_response.outputs[0]
        return np.asarray(output.data).reshape(output.shape)

    def detect_objects(self, image, threshold=0.5, needs_preprocessing=False, temp_path='temp.jpg'):
        """Detect objects in an image for this service. Only works when deploying an object detection
            model like YOLO or SSD.

        # Argments
            image: `numpy.ndarray`. Input image to detect objects from.
            threshold: floating point between 0 and 1. bounding box threshold, only objects with at
                least this threshold get returned.
            needs_preprocessing: boolean. whether input data needs pre-processing
            temp_path: local path to which intermediate numpy arrays get stored.

        # Returns
            `DetectionResult`, a Python dictionary with labels, confidences and locations of bounding boxes
                of detected objects.
        """
        if cv2 is None:
            raise Exception("OpenCV is not installed.")
        cv2.imwrite(temp_path, image)
        url = 'http://{}/endpoints/{}/model/{}/v{}/detectobjects'.format(
            self.skil.config.host,
            self.model.deployment.name,
            self.model.name,
            self.model.version
        )

        # TODO: use the official "detectobject" client API, once fixed in skil_client
        # print(">>>> TEST")
        # resp = self.skil.api.detectobjects(
        #     id='foo',
        #     needs_preprocessing=False,
        #     threshold='0.5',
        #     image_file=temp_path,
        #     deployment_name=self.model.deployment.name,
        #     version_name='default',
        #     model_name=self.model.name
        # )

        with open(temp_path, 'rb') as data:
            resp = requests.post(
                url=url,
                headers=self.skil.auth_headers,
                files={
                    'file': (temp_path, data, 'image/jpeg')
                },
                data={
                    'id': self.model.id,
                    'needs_preprocessing': 'true' if needs_preprocessing else 'false',
                    'threshold': str(threshold)
                }
            )
        if os.path.isfile(temp_path):
            os.remove(temp_path)

        return json.loads(resp.content)
