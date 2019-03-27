# InferenceVerticleConfiguration.java (SKIL)
# PubsubConfig.java (SKIL)

from .model_loading_config import HandlerType
from .model_loading_config import ModelLoadingconfig
from .input_handler_config import InputDataType
from .input_handler_config import OutputType
from .input_handler_config import ResponseOutputType
from .model_server_inference_config import ModelServerInferenceConfig


class PubsubConfig(object):
    def __init__(self,
                 httpMethod=None,
                 pubsubUrl=None,
                 contentType=None):
        if httpMethod is not None:
            assert isinstance(httpMethod, str)
        self.httpMethod = httpMethod

        if pubsubUrl is not None:
            assert isinstance(pubsubUrl, str)
        self.pubsubUrl = pubsubUrl

        if contentType is not None:
            assert isinstance(contentType, str)
        self.contentType = contentType

    def tojson(self):
        j = self.__dict__.copy()
        j["@class"] = "ai.skymind.modelserver.config.PubsubConfig"
        return j


class InferenceVerticleConfiguration(object):
    def __init__(self,
                 objectDetectionLabelsPath=None,
                 inferenceLoadingConfigKey=None,
                 modelLoadingConfig=None,
                 pmmlEvaluatorFactoryClassKey=None,
                 pmmlPathKey=None,
                 schemaKey=None,
                 transformProcessKey=None,
                 imageTransformProcessKey=None,
                 handlerTypeKey=None,
                 outputsKey=None,
                 inputDataType=None,
                 dimensionsConfigKey=None,
                 outputTypeKey=None,
                 normalizationLoadingconfig=None,
                 objectDetectionThreshold=0.0,
                 objectDetectionNumLabels=0,
                 opPreProcessing=None,
                 opPostProcessing=None,
                 ResponseOutputType=None,
                 originalImageHeight=0,
                 originalImageWidth=0,
                 httpPort=0,
                 addRetrainEndpoints=False,
                 preprocessingInputNames=None,
                 preProcessingOutputNames=None,
                 postProcessingInputNames=None,
                 postProcessingOutputNames=None,
                 unkVectorPath=None
                 ):
        if objectDetectionLabelsPath is not None:
            assert isinstance(objectDetectionLabelsPath, str)
        self.objectDetectionLabelsPath = objectDetectionLabelsPath

        if inferenceLoadingConfigKey is not None:
            assert isinstance(inferenceLoadingConfigKey, ModelServerInferenceConfig)
        self.inferenceLoadingConfigKey = inferenceLoadingConfigKey

        if modelLoadingConfig is not None:
            assert isinstance(modelLoadingConfig, ModelLoadingconfig)
        self.modelLoadingConfig = modelLoadingConfig

        #TODO