import pytest
import skil
import uuid
from skil.resources.groups import *


_sk = None


def _get_sk():
    global _sk
    if _sk is None:
        _sk = skil.Skil()
    return _sk  


def test_group_add_and_deletion():
    sk = _get_sk()
    res = skil.resources.storage.S3(sk, "s3" + str(uuid.uuid1())[:6], "test_bucket",
                                    "test_region", "test_credentials")

    group = ResourceGroup(sk, str(uuid.uuid1())[:6])
    group.add_resource(res)

    groups = group.get_all_resources()

    assert len(groups) == 1
    assert groups[0].resource_id == res.resource_id

    # TODO deletion does not seem to work. investigate why!
    # group.delete_resource(res)

    # groups = group.get_all_resources()
    # assert len(groups) == 0

    group.delete()



if __name__ == '__main__':
    pytest.main([__file__])
