# An abstract class to make sure that you don't shoot yourself in the foot

class MockJavaClass(object):

    def __init__(self):
        if self.__class__ == MockJavaClass:
            raise Exception("Abstract class!")
        self._check_types(self.__dict__)

    def _check_types(self, obj):
        if isinstance(obj, list):
            for x in obj:
                self._check_types(x)
        elif isinstance(obj, dict):
            for k in obj.keys():
                assert isinstance(k, str), "Only str keys allowed"
            for x in obj.values():
                self._check_types(x)
        else:
            allowed_types = (
                int,
                float,
                str,
                MockJavaClass,
                type(None),
            )
            assert isinstance(obj, allowed_types)

    def _recursive_serialize(self, obj):
        if isinstance(obj, MockJavaClass):
            return obj.tojson()
        elif isinstance(obj, list):
            return [self._recursive_serialize(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: self._recursive_serialize(obj[k]) for k in obj}
        else:
            return obj

    def tojson(self):
        j = self.__dict__.copy()
        self._check_types(j) # attributes might have been set manually
        j["@class"] = self.java_class
        for k in j:
            j[k] = self._recursive_serialize(j[k])
        return j
