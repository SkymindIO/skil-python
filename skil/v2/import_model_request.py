from .mock_java_class import MockJavaClass


class ImportModelRequest(MockJavaClass):

    java_class = "io.skymind.deployment.rest.ImportModelRequest"

    def __init__(self,
                 name,
                 scale,
                 uri=None,
                 modelType=None,
                 fileLocation=None,
                 jvmArgs=None,
                 subType=None,
                 labelsFileLocation=None,
                 extraArgs=None,
                 etlJson=None,
                 inputNames=None,
                 outputNames=None,
                 modelInstanceId=None,
                 modelServerV2ConfigFileLocation=None,
                 modelHistoryId=None):
        assert isinstance(name, str)
        self.name = name
        assert isinstance(scale, int)
        self.scale = scale

        if uri is not None:
            assert isinstance(uri, (str, list))
        self.uri = uri

        if modelType is None:
            raise Exception("modelType not provided")
        assert isinstance(modelType, str)
        self.modelType = modelType

        if fileLocation is not None:
            assert isinstance(fileLocation, str)
        self.fileLocation = fileLocation

        if jvmArgs is not None:
            assert isinstance(jvmArgs, str)
        self.jvmArgs = jvmArgs

        if subType is not None:
            assert isinstance(subType, str)
        self.subType = subType

        if labelsFileLocation is not None:
            assert isinstance(labelsFileLocation, str)
        self.labelsFileLocation = labelsFileLocation

        if extraArgs is not None:
            assert isinstance(extraArgs, str)
        self.extraArgs = extraArgs

        if etlJson is not None:
            assert isinstance(etlJson, str)
        self.etlJson = etlJson

        if inputNames is not None:
            assert isinstance(inputNames, list)
            for x in inputNames:
                assert isinstance(x, str)
        self.inputNames = inputNames

        if outputNames is not None:
            assert isinstance(outputNames, list)
            for x in outputNames:
                assert isinstance(x, str)
        self.outputNames = outputNames

        if modelInstanceId is not None:
            assert isinstance(modelInstanceId, str)
        self.modelInstanceId = modelInstanceId

        if modelServerV2ConfigFileLocation is not None:
            assert isinstance(modelServerV2ConfigFileLocation, str)
        self.modelServerV2ConfigFileLocation = modelServerV2ConfigFileLocation

        if modelHistoryId is not None:
            assert isinstance(modelHistoryId, str)
        self.modelHistoryId = modelHistoryId

        super(ImportModelRequest, self).__init__()
