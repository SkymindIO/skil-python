from.common import get_resource_by_id


class ResourceGroup:
    '''ResourceGroup

    SKIL resource groups can be used to group skil.resources.base.Resource instances
    into logical groups. You first create a group and then add resources to the group
    later on, using `add_resource`.

    # Arguments:
        skil: `Skil` server instance
        group_name: Name of the resource group
        group_id: optional group ID to retrieve an existing resource group
        create: boolean, for internal use only. whether to create a new resource or not
    '''

    def __init__(self, skil, group_name, group_id=None, create=True):
        self.skil = skil
        self.group_name = group_name
        self.group_id = group_id

        if create:
            resp = self.skil.api.add_resource_group(group_name)
            self.group_id = resp.group_id
        else:
            if group_id is None:
                raise ValueError(
                    'If create is False you need to provide a valid group_id')

    def add_resource(self, resource):
        '''Add a skil.resource.base.Resource to this group
        '''
        self.skil.api.add_resource_to_group(
            self.group_id, resource.resource_id)

    def delete_resource(self, resource):
        '''Delete a skil.resource.base.Resource from this group
        '''
        self.skil.api.delete_resource_from_group(
            self.group_id, resource.resource_id)

    def delete(self):
        '''Delete this resource group.
        '''
        self.skil.api.delete_resource_group_by_id(self.group_id)

    def get_all_resources(self):
        '''Get all resources attached to this group
        '''
        resp = self.skil.api.get_resources_from_group(self.group_id)
        return [get_resource_by_id(self.skil, res.resource_id) for res in resp]


def delete_resource_group_by_id(skil, group_id):
    skil.api.delete_resource_group_by_id(group_id)


def get_resource_group_by_id(skil, group_id):
    resp = skil.api.get_resource_group_by_id(group_id)
    return ResourceGroup(skil, resp.group_name, resp.group_id, False)


def get_all_resource_groups(skil):
    resp = skil.api.get_resource_groups()
    return [get_resource_group_by_id(skil, group.group_id) for group in resp]


def get_resources_from_group(skil, group):
    resp = skil.api.get_resources_from_group(group.group_id)
    return [get_resource_by_id(skil, res.resource_id) for res in resp]
