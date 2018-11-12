import abc
import skil_client

class DataResource:
    """DataResource

    A SKIL data resource is an abstraction for (cloud)
    storage capabilities, including systems like AWS S3,
    HDFS, Azure Storage or Google Cloud storage.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Adds the data resource to SKIL.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self):
        """Delete the data resource from SKIL.
        """
        raise NotImplementedError