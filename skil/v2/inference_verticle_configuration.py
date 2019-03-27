# InferenceVerticleConfiguration.java (SKIL)
# PubsubConfig.java (SKIL)

from .model_loading_config import HandlerType
from .model_loading_config import ModelLoadingConfig
from .input_handler_config import InputDataType
from .input_handler_config import OutputType
from .input_handler_config import ResponseOutputType
from .model_server_inference_config import ModelServerInferenceConfig
from .schema import Schema
from .mock_java_class import MockJavaClass


class PubsubConfig(MockJavaClass):

    java_class = "ai.skymind.modelserver.config.PubsubConfig"

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

class InferenceVerticleConfiguration(MockJavaClass):

    java_class = "ai.skymind.modelserver.verticles.constants.InferenceVerticleConfiguration"

    def __init__(self,
                 objectDetectionLabelsPath=None,
                 inferenceLoadingConfigKey=None,
                 modelLoadingConfig=None,
                 pmmlEvaluatorFactoryClassKey=None,
                 pmmlPathKey=None,
                 schemaKey=None,
                 transformProcessKey=None,
                 imageTransformProcessKey=None,
                 pubsubConfig=None,
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
                 responseOutputFormat=None,
                 originalImageHeight=0,
                 originalImageWidth=0,
                 httpPort=0,
                 addRetrainEndpoints=False,
                 preProcessingInputNames=None,
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
            assert isinstance(modelLoadingConfig, ModelLoadingConfig)
        self.modelLoadingConfig = modelLoadingConfig

        if pmmlEvaluatorFactoryClassKey is not None:
            assert isinstance(pmmlEvaluatorFactoryClassKey, str)
        self.pmmlEvaluatorFactoryClassKey = pmmlEvaluatorFactoryClassKey

        if pmmlPathKey is not None:
            assert isinstance(pmmlPathKey, str)
        self.pmmlPathKey = pmmlPathKey

        if schemaKey is not None:
            assert isinstance(schemaKey, Schema)
        self.schemaKey = schemaKey

        if transformProcessKey is not None:
            raise NotImplementedError
        self.transformProcessKey = transformProcessKey

        if imageTransformProcessKey is not None:
            raise NotImplementedError
        self.imageTransformProcessKey = imageTransformProcessKey

        if pubsubConfig is not None:
            assert isinstance(pubsubConfig, PubsubConfig)
        self.pubsubConfig = pubsubConfig

        if handlerTypeKey is not None:
            assert isinstance(handlerTypeKey, HandlerType)
        self.handlerTypeKey = handlerTypeKey

        if outputsKey is not None:
            assert isinstance(outputsKey, Schema)
        self.outputsKey = outputsKey

        if inputDataType is not None:
            assert hasattr(InputDataType, inputDataType)
        self.inputDataType = inputDataType

        if dimensionsConfigKey is not None:
            assert isinstance(dimensionsConfigKey, dict)
            for k, v in dimensionsConfigKey.items():
                assert isinstance(k, str)
                assert isinstance(v, list)
                for d in v:
                    assert isinstance(d, int)
        self.dimensionsConfigKey = dimensionsConfigKey

        if outputTypeKey is not None:
            assert hasattr(OutputType, outputTypeKey)
        self.outputTypeKey = outputTypeKey

        if normalizationLoadingconfig is not None:
            assert isinstance(normalizationLoadingconfig, dict)
            for k, v in normalizationLoadingconfig.items():
                assert isinstance(k, str)
                assert isinstance(v, str)
        self.normalizationLoadingconfig = normalizationLoadingconfig

        assert isinstance(objectDetectionThreshold, float)
        self.objectDetectionThreshold = objectDetectionThreshold
        assert isinstance(objectDetectionNumLabels, int)
        self.objectDetectionNumLabels = objectDetectionNumLabels

        if opPreProcessing is not None:
            assert isinstance(opPreProcessing, str)
        self.opPreProcessing = opPreProcessing

        if opPostProcessing is not None:
            assert isinstance(opPostProcessing, str)
        self.opPostProcessing = opPostProcessing

        if responseOutputFormat is not None:
            assert hasattr(responseOutputFormat, ResponseOutputType)
        self.responseOutputFormat = responseOutputFormat

        assert isinstance(originalImageHeight, int)
        self.originalImageHeight = originalImageHeight
        assert isinstance(originalImageWidth, int)
        self.originalImageWidth = originalImageWidth

        assert isinstance(httpPort, int)
        self.httpPort = httpPort

        assert isinstance(addRetrainEndpoints, bool)
        self.addRetrainEndpoints = addRetrainEndpoints

        def assert_list_of_string(obj):
            if obj is None:
                return
            assert isinstance(obj, list)
            for x in obj:
                assert isinstance(x, str)
        
        assert_list_of_string(preProcessingInputNames)
        self.preProcessingInputNames = preProcessingInputNames
        assert_list_of_string(preProcessingOutputNames)
        self.preProcessingOutputNames = preProcessingOutputNames
        assert_list_of_string(postProcessingInputNames)
        self.postProcessingInputNames = postProcessingInputNames
        assert_list_of_string(postProcessingOutputNames)
        self.postProcessingOutputNames = postProcessingOutputNames

        if unkVectorPath is not None:
            assert isinstance(unkVectorPath, str)
        self.unkVectorPath = unkVectorPath

        super(InferenceVerticleConfiguration, self).__init__()
