# EvalConfig.java (SKIL)
# InferenceMode.java (DL4J)
from .mock_java_class import MockJavaClass
import uuid


class EvalType:
    ROC_BINARY = "ROC_BINARY"
    ROC = "ROC"
    EVALUATION_BINARY = "EVALUATION_BINARY"
    EVALUATION = "EVALUATION"
    REGRESSON_EVALUATION = "REGRESSON_EVALUATION"
    ROC_MULTI_CLASS = "ROC_MULTI_CLASS"


class EvalConfig(MockJavaClass):

    java_class = "ai.skymind.modelserver.retrain.EvalConfig"

    def __init__(self,
                 inputs=None,
                 testSet=None,
                 testLabels=None,
                 evalType=None,
                 metric=None,
                 numClassesForEval=0,
                 rocThresholdSteps=0,
                 decisionThreshold=None,
                 arrayType="numpy",
                 modelHistoryUrl=None,
                 modelInstanceId=None,
                 experimentId=str(uuid.uuid1())):
        if inputs is not None:
            assert isinstance(inputs, list)
            for inp in inputs:
                assert isinstance(inp, str)
        self.inputs = inputs

        if testSet is not None:
            assert isinstance(testSet, dict)
            for k, v in testSet.items():
                assert isinstance(k, str)
                assert isinstance(v, str)
        self.testSet = testSet

        if testLabels is not None:
            assert isinstance(testLabels, str)
        self.testLabels = testLabels

        if evalType is not None:
            assert hasattr(EvalType, evalType)
        self.evalType = EvalType

        if metric is not None:
            assert isinstance(metric, str)
        self.metric = metric

        assert isinstance(numClassesForEval, int)
        self.numClassesForEval = numClassesForEval
        assert isinstance(rocThresholdSteps, int)
        self.rocThresholdSteps = rocThresholdSteps
        
        if decisionThreshold is not None:
            assert isinstance(decisionThreshold, str)

        assert isinstance(arrayType, str)
        self.arrayType = arrayType

        if modelHistoryUrl is not None:
            assert isinstance(modelHistoryUrl, str)
        self.modelHistoryUrl = modelHistoryUrl

        if modelInstanceId is not None:
            assert isinstance(modelInstanceId, str)
        self.modelInstanceId = modelInstanceId

        assert isinstance(experimentId, str)
        self.experimentId = experimentId

        super(EvalConfig, self).__init__()
