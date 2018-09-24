import sys
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock

import skil


@mock.patch('skil.Skil')
def test_skil_mock(Skil):
    assert Skil is skil.Skil
    skil_server = Skil()
    assert Skil.called

    skil_server.get_default_server_id = mock.MagicMock(return_value=1337)
    skil_server.get_default_server_id()


@mock.patch('skil.Skil')
def test_model_upload(Skil):
    skil_server = Skil()

    model_file_name = './dummy.pb'
    skil_server.upload_model(model_file_name)
