import os
import sys
import pytest
from skil import Model
if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock as mock


@mock.patch('skil.Skil')
def test_skil_default_model(Skil):
    with open('dummy', 'w') as f:
        f.write('foo')
    model = Model('dummy')
    model.add_evaluation(eval_id='eval', name='eval', version=1, accuracy=0.93)
    os.remove('dummy')


if __name__ == '__main__':
    pytest.main([__file__])
