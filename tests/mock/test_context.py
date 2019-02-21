import pytest
from six import text_type as unicode
import sys


def test_unicode_instance():
    file_path = '/foo'
    if isinstance(file_path, unicode):
        file_path = file_path.encode(sys.getfilesystemencoding())


if __name__ == '__main__':
    pytest.main([__file__])
