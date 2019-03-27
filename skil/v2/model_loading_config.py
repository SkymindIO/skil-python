# ModelLoadingconfig.java
# ModelConfigType.java


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


class ModelConfigType(object):
    def __init__(self, modelLoadingPath, outputAdapterType, modelType, schemaJson):
        if modelLoadingPath is None:
            modelLoadingPath = ""
        assert isinstance(modelLoadingPath, str)
        self.modelLoadingPath = modelLoadingPath
        assert hasattr(OutputAdapterType, outputAdapterType), "Invalid OutputAdapterType"
        self.outputAdapterType = outputAdapterType
        assert hasattr(ModelType, modelType), "Invalid ModelType"
        self.modelType = modelType
        self.schemaJson = schemaJson

    def tojson(self):
        j = {}
        j["@class"] = "ai.skymind.modelserver.verticles.ModelConfigType"
        j["modelLoadingPath"] = self.modelLoadingPath
        j["outputAdapterType"] = self.outputAdapterType
        j["modelType"] = self.modelType
        j["schemaJson"] = self.schemaJson
        return j


class ModelLoadingconfig(object):
    def __init__(self, modelConfigTypes):
        assert isinstance(modelConfigTypes, list)
        for mct in modelConfigTypes:
            assert isinstance(mct, ModelConfigType)
        self.modelConfigTypes = modelConfigTypes

    def tojson(self):
        j = {}
        j["@class"] = "ai.skymind.modelserver.config.ModelLoadingConfig"
        j["modelConfigTypes"] = [mct.tojson() for mct in self.modelConfigTypes]
        return j
