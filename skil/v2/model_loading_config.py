# ModelLoadingconfig.java
# ModelConfigType.java


from .mock_java_class import MockJavaClass

class HandlerType:
    CSV = "CSV"
    DICTIONARY = "DICTIONARY"
    CSVPUBSUB = "CSVPUBSUB"
    DICTIONARYPUBSUB = "DICTIONARYPUBSUB"
    CSV_ERROR = "CSV_ERROR"
    DICTIONARY_ERROR = "DICTIONARY_ERROR"
    CSVPUBSUB_ERROR = "CSVPUBSUB_ERROR"
    DICTIONARYPUBSUB_ERROR = "DICTIONARYPUBSUB_ERROR"


class ModelType:
    COMPUTATION_GRAPH = "COMPUTATION_GRAPH"
    MULTILAYERNETWORK = "MULTILAYERNETWORK"
    PMML =  "PMML"
    TENSORFLOW = "TENSORFLOW"
    KERAS = "KERAS"
    SAMEDIFF = "SAMEDIFF"


class OutputAdapterType:
    REGRESSION = "REGRESSION"
    CLASSIFICATION = "CLASSIFICATION"
    RAW = "RAW"


class ModelConfigType(MockJavaClass):

    java_class = "ai.skymind.modelserver.verticles.ModelConfigType"

    def __init__(self, modelLoadingPath, outputAdapterType, modelType, schemaJson=None):
        if modelLoadingPath is None:
            modelLoadingPath = ""
        assert isinstance(modelLoadingPath, str)
        self.modelLoadingPath = modelLoadingPath
        assert hasattr(OutputAdapterType, outputAdapterType), "Invalid OutputAdapterType"
        self.outputAdapterType = outputAdapterType
        assert hasattr(ModelType, modelType), "Invalid ModelType"
        self.modelType = modelType
        if schemaJson is not None:
            assert isinstance(schemaJson, str)
        self.schemaJson = schemaJson
        super(ModelConfigType, self).__init__()


class ModelLoadingConfig(MockJavaClass):

    java_class = "ai.skymind.modelserver.config.ModelLoadingConfig"

    def __init__(self, modelConfigTypes):
        assert isinstance(modelConfigTypes, list)
        for mct in modelConfigTypes:
            assert isinstance(mct, ModelConfigType)
        self.modelConfigTypes = modelConfigTypes
        super(ModelLoadingConfig, self).__init__()

