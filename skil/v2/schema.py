
_AVAILABLE_COLUMN_TYPES = [
    "Boolean",
    "Categorical",
    "Double",
    "Float",
    "Integer",
    "Long",
    "NDArray",
    "String",
    "Time"
]

class Schema(object):

    def __init__(self):
        self.columns = []

    def add_boolean(self, name):
        self.columns.append((name, "Boolean"))

    def add_categorical(self, name, categories):
        self.columns.append((name, "Categorical", categories))

    def add_double(self, name):
        self.columns.append((name, "Double"))

    def add_float(self, name):
        self.columns.append((name, "Float"))

    def add_integer(self, name):
        self.columns.append((name, "Integer"))

    def add_long(self, name):
        self.columns.append((name,"Long"))

    def add_ndarray(self, name, shape):
        self.columns.append((name, "NDArray", shape))

    def add_string(self, name):
        self.columns.append((name, "String"))

    def add_time(self, name):
        raise NotImplementedError
        self.columns.append((name, "Time"))

    def tojson(self):
        j = {}
        j["@class"] = "org.datavec.api.transform.schema.Schema"
        columns = []
        for col in self.columns:
            col_type = col[1]
            cj = {}
            cj["@class"] = "org.datavec.api.transform.metadata.{}MetaData".format(col_type)
            cj["name"] = col[0]
            if col_type == "Categorical":
                cj["stateNames"] = col[2]
            elif col_type == "NDArray":
                cj["shape"] = list(col[2])
            elif col_type in ["Double", "Float"]:
                cj["allowInfinite"] = False
                cj["allowNaN"] = False
            columns.append(cj)
        j["columns"] = columns
        return j

