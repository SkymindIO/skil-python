# ModelServerInferenceConfig.java

from .eval_config import EvalConfig

class InferenceMode:
    SEQUENTIAL = "SEQUENTIAL"
    BATCHED = "BATCHED"
    INPLACE = "INPLACE"
    DEFAULT_INFERENCE_MODE = BATCHED


class ModelServerInferenceConfig(object):

    def __init__(self,
                 queueLimit=0,
                 batchLimit=0,
                 workers=0,
                 maxTrainEpochs=1,
                 inferenceMode=None,
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

    def tojson(self):
        j = self.__dict__.copy()
        j["evalConfig"] = j["evalConfig"].tojson()
        j["@class"] = "ai.skymind.modelserver.inference.config.ModelServerInferenceConfig"
        return j
