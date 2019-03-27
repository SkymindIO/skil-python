# InputHandlerConfig.java

class OutputType:
    CLASSIFICATION = "CLASSIFICATION"
    YOLO = "YOLO"
    SSD = "SSD"
    RCNN = "RCNN"
    RAW = "RAW"
    REGRESSION = "REGRESSION"


class ResponseOutputType:
    ND4J = "ND4J"
    NUMPY = "NUMPY"
    ARROW = "ARROW"
    JSON = "JSON"


class InputDataType:
    IMAGE = "IMAGE"
    NUMPY = "NUMPY"
    NDARRAY = "NDARRAY"
    JSON = "JSON"
