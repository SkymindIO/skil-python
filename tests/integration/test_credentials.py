from skil.resources.credentials import *
import pytest


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
    with pytest.raises(Exception):
        delete_credentials_by_id(sk, cred_id)


def test_aws_creds():
    sk = _get_sk()
    aws = AWS(sk, "uri")
    aws.delete()


if __name__ == '__main__':
    pytest.main([__file__])
