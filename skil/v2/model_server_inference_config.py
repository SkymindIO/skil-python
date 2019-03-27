# ModelServerInferenceConfig.java

from .eval_config import EvalConfig
from .mock_java_class import MockJavaClass


class InferenceMode:
    SEQUENTIAL = "SEQUENTIAL"
    BATCHED = "BATCHED"
    INPLACE = "INPLACE"
    DEFAULT_INFERENCE_MODE = BATCHED


class ModelServerInferenceConfig(MockJavaClass):

    java_class = "ai.skymind.modelserver.inference.config.ModelServerInferenceConfig"

    def __init__(self,
                 queueLimit=64,
                 batchLimit=32,
                 workers=1,
                 maxTrainEpochs=1,
                 inferenceMode=InferenceMode.DEFAULT_INFERENCE_MODE,
                 retrainBatchSize=1,
                 retrainDataBound=1,
                 retrainModelWithInference=False,
                 evalConfig=None,
                 vertxConfigJson=None
                 ):
        assert isinstance(queueLimit, int)
        self.queueLimit = queueLimit
        assert isinstance(batchLimit, int)
        self.batchLimit = batchLimit
        assert isinstance(workers, int)
        self.workers = workers
        assert isinstance(maxTrainEpochs, int)
        self.maxTrainEpochs = maxTrainEpochs

        if inferenceMode is not None:
            assert hasattr(InferenceMode, inferenceMode)
        self.inferenceMode = inferenceMode

        assert isinstance(retrainBatchSize, int)
        self.retrainBatchSize = retrainBatchSize
        assert isinstance(retrainDataBound, int)
        self.retrainDataBound = retrainDataBound

        assert isinstance(retrainModelWithInference, bool)
        self.retrainModelWithInference = retrainModelWithInference

        if evalConfig is not None:
            assert isinstance(evalConfig, EvalConfig)
        self.evalConfig = evalConfig

        if vertxConfigJson is not None:
            assert isinstance(vertxConfigJson, str)
        self.vertxConfigJson = vertxConfigJson

        super(ModelServerInferenceConfig, self).__init__()

    @staticmethod
    def defaultConfig():
        return ModelServerInferenceConfig()
