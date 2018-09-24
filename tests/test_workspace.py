from skil import WorkSpace
import sys
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock


@mock.patch('skil.Skil')
def test_work_space(Skil):
    skil_server = Skil()
    ws = WorkSpace(skil_server)
