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
    """A service is a deployed model.

    # Arguments:
        skil: `Skil` server instance
        model: `skil.Model` instance
        deployment: `skil.Deployment` instance
        model_deployment: result of `deploy_model` SKIL API call of a `Model`
    """
    __metaclass__ = type

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

    def predict(self, data, version='default'):
        """Predict for given batch of data.

        # Arguments:
            data: `numpy.ndarray` (or list thereof). Batch of input data, or list of batches for multi-input model.
            version: version of the deployed service

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
            version_name=version,
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

    def predict_single(self, data, version='default'):
        """Predict for a single input.

        # Arguments:
            data: `numpy.ndarray` (or list thereof). Input data.
            version: version of the deployed service

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
            version_name=version,
            body=skil_client.MultiPredictRequest(
                id=str(uuid.uuid1()),
                needs_pre_processing=False,
                inputs=inputs
            )
        )
        # TODO should support multi-out
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
                # TODO: should also have a model "version"?
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


class TransformCsvService(Service):
    """TransformCsvService

    A service for transforming CSV data

    # Arguments:
        skil: `Skil` server instance
        model: `skil.Model` instance
        deployment: `skil.Deployment` instance
        model_deployment: result of `deploy_model` API call of a model
    """

    def __init__(self, skil, model, deployment, model_deployment):
        super(TransformCsvService, self).__init__(
            skil, model, deployment, model_deployment)

    @staticmethod
    def _to_single_csv_record(data, separator):
        return skil_client.SingleCSVRecord(data.split(separator))

    @staticmethod
    def _to_batch_csv_record(data, separator):
        single_records = [
            TransformCsvService._to_single_csv_record(d, separator) for d in data]
        return skil_client.BatchCSVRecord(single_records)

    def predict(self, data, separator=',', version='default'):
        """Predict for given batch of data.

        # Arguments
            data: list of list of strings, where a list of strings represents a single csv record
            version: version of the deployed service

        # Returns
            skil_client.BatchCSVRecord
        """
        batch_record = self._to_batch_csv_record(data, separator)

        return self.skil.api.transform_csv(
            deployment_name=self.deployment.name,
            transform_name=self.model_name,
            version_name=version,
            batch_csv_record=batch_record
        )

    def predict_single(self, data, separator=',', version='default'):
        """Predict a single input.

        # Arguments
            data: a list of strings, where a list of strings represents a single csv record
            version: version of the deployed service

        # Returns
            skil_client.SingleCSVRecord
        """
        single_record = self._to_single_csv_record(data, separator)
        return self.skil.api.transformincremental_csv(
            deployment_name=self.deployment.name,
            transform_name=self.model_name,
            version_name=version,
            single_csv_record=single_record
        )


class TransformArrayService(Service):
    """A service for transforming array data

    # Arguments:
        skil: `Skil` server instance
        model: `skil.Model` instance
        deployment: `skil.Deployment` instance
        model_deployment: result of `deploy_model` API call of a model
    """

    def __init__(self, skil, model, deployment, model_deployment):
        super(TransformArrayService, self).__init__(
            skil, model, deployment, model_deployment)

    def predict(self, data, version='default'):
        """Predict for given batch of data.

        # Arguments
            data: BatchRecord object # TODO figure out what this is / how it works
            version: version of the deployed service

        # Returns
            skil_client.Base64NDArrayBody
        """
        return self.skil.api.transformarray(
            deployment_name=self.deployment.name,
            transform_name=self.model_name,
            version_name=version,
            batch_record=data
        )

    def predict_single(self, data, version='default'):
        """Predict a single input.

        # Arguments:
            data: SingleRecord object # TODO figure out what this is / how it works
            version: version of the deployed service

        # Returns
            skil_client.Base64NDArrayBody
        """
        return self.skil.api.transformincrementalarray(
            deployment_name=self.deployment.name,
            transform_name=self.model_name,
            version_name=version,
            single_record=data
        )


class TransformImageService(Service):
    """A service for transforming array data

    # Arguments:
        skil: `Skil` server instance
        model: `skil.Model` instance
        deployment: `skil.Deployment` instance
        model_deployment: result of `deploy_model` API call of a model
    """

    def __init__(self, skil, model, deployment, model_deployment):
        super(TransformImageService, self).__init__(
            skil, model, deployment, model_deployment)

    def predict(self, data, version='default'):
        """Predict for given batch of data.

        # Arguments
            data: list of files that contain the actual image data
            version: version of the deployed service

        # Returns
            skil_client.Base64NDArrayBody
        """
        return self.skil.api.transformimage(
            deployment_name=self.deployment.name,
            image_transform_name=self.model_name,
            version_name=version,
            files=data
        )

    def predict_single(self, data, version='default'):
        """Predict a single input

        # Arguments
            data: file that contains the actual image data
            version: version of the deployed service

        # Returns
            skil_client.Base64NDArrayBody
        """
        return self.skil.api.transformincrementalimage(
            deployment_name=self.deployment.name,
            image_transform_name=self.model_name,
            version_name=version,
            file=data
        )


class Pipeline(Service):
    """Pipeline

    SKIL pipeline abstraction, used for chaining transform steps and
    models.

    # Arguments:
        deployment: skil.Deployment instance
        model: skil.Model instance
        transform: skil.Transform instance (optional)
        start_server: boolean. If `True`, the service is immediately started.
        scale: integer. Scale-out for deployment.
        input_names: list of strings. Input variable names of the model.
        output_names: list of strings. Output variable names of the model.
        verbose: boolean. If `True`, api response will be printed.

    """

    def __init__(self, skil, deployment, model, transform=None,
                 start_server=True, scale=1, input_names=None,
                 output_names=None, verbose=True):

        super(Pipeline, self).__init__(self, model.skil, deployment, None)

        self.model_service = model.deploy(
            deployment, start_server, scale, input_names, output_names, verbose
        )
        self.transform_service = transform.deploy(
            deployment, start_server, scale, input_names, output_names, verbose
        )

    def start(self):
        """Start service """
        self.model_service.start()
        self.transform_service.start()

    def stop(self):
        """Stop service """
        self.model_service.stop()
        self.transform_service.stop()

    def predict(self, data, version='default'):
        """Predict for given batch of data.

        # Arguments:
            data: `numpy.ndarray` (or list thereof). Batch of input data, or list of batches for multi-input model.

        # Returns
            `numpy.ndarray` instance for single output model and list of `numpy.ndarray` for multi-output model.
        """
        if self.transform_service:
            data = self.transform_service.predict(data, version)
        return self.model_service.predict(data, version)

    def predict_single(self, data, version='default'):
        """Predict for a single input.

        # Arguments:
            data: `numpy.ndarray` (or list thereof). Input data.

        # Returns
            `numpy.ndarray` instance for single output model and list of `numpy.ndarray` for multi-output model.
        """
        if self.transform_service:
            data = self.transform_service.predict_single(data, version)
        return self.model_service.predict_single(data, version)

    def detect_objects(self, image, threshold=0.5, needs_preprocessing=False, temp_path='temp.jpg',
                       version='default'):
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
        if self.transform_service:
            image = self.transform_service.predict_single(image, version)
        return self.model_service.detect_objects(image, threshold, needs_preprocessing, temp_path)
