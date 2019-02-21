from skil.resources.credentials import *
import pytest
import skil
import uuid
import time

_sk = None


def _get_sk():
    global _sk
    if _sk is None:
        _sk = skil.Skil()
    return _sk


def test_creation_deletion():
    sk = _get_sk()
    cred = Credentials(sk, "AWS", "uri", "name")
    cred_id = cred.id
    rep_cred = get_credentials_by_id(sk, cred_id)
    assert rep_cred.id == cred_id

    rep_cred.delete()
    time.sleep(1)
    with pytest.raises(Exception):
        delete_credentials_by_id(sk, cred_id)


def test_aws_creds():
    sk = _get_sk()
    cred = AWS(sk, "uri_" + str(uuid.uuid1())
               [:6], "name_" + str(uuid.uuid1())[:6])
    cred.delete()


def test_azure_creds():
    sk = _get_sk()
    cred = Azure(sk, "uri" + str(uuid.uuid1())
                 [:6], "name_" + str(uuid.uuid1())[:6])
    cred.delete()


def test_gce_creds():
    sk = _get_sk()
    cred = GoogleCloud(sk, "uri" + str(uuid.uuid1())
                       [:6], "name_" + str(uuid.uuid1())[:6])
    cred.delete()


def test_hadoop_creds():
    sk = _get_sk()
    cred = Hadoop(sk, "uri" + str(uuid.uuid1())
                  [:6], "name_" + str(uuid.uuid1())[:6])
    cred.delete()


if __name__ == '__main__':
    pytest.main([__file__])
