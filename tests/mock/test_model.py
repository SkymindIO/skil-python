import sys
from skil import Model
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock


@mock.patch('skil.Skil')
def test_skil_default_model(Skil):
    model = Model('dummy_file_name')
    model.add_evaluation(id='eval', name='eval', version=1, accuracy=0.93)
    model.deploy()
    # model.serve() TODO need to mock api response for this one
