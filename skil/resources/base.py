class Resource:
    """Resource

    A SKIL  resource is an abstraction for (cloud and on-premise)
    compute or storage capabilities.
    """
    __metaclass__ = type

    def __init__(self, skil, resource_id=None, *args, **kwargs):
        """Add the resource to SKIL.
        """
        self.skil = skil
        self.resource_id = resource_id

    def delete(self):
        """Delete the resource from SKIL.
        """
        if self.resource_id:
            self.skil.api.delete_resource_by_id(resource_id=self.resource_id)
