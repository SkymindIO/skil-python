from unittest.mock import patch, MagicMock
import skil


@patch('skil.Skil')
def test_skil_mock(Skil):
    assert Skil is skil.Skil
    skil_server = Skil()
    assert Skil.called

    skil_server.get_default_server_id = MagicMock(return_value=1337)
    skil_server.get_default_server_id()


@patch('skil.Skil')
def test_model_upload(Skil):
    skil_server = Skil()

    model_file_name = './dummy.pb'
    skil_server.upload_model(model_file_name)
