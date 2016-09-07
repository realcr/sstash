import os
import shutil
import tempfile
import pytest


@pytest.fixture(scope='function')
def tmp_dir_path(request):
    """
    Give a path for a temporary directory
    The directory is destroyed at the end of the test.
    """
    # Temporary directory.
    tmp_dir = tempfile.mkdtemp()

    def teardown():
        # Delete the whole directory:
        shutil.rmtree(tmp_dir)

    request.addfinalizer(teardown)
    return tmp_dir


@pytest.fixture(scope='function')
def tmp_file_path(request,tmp_dir_path):
    """
    Give a path for a temporary file.
    The file is destroyed at the end of the test.
    """
    # Temporary file path:
    tmp_file_path = os.path.join(tmp_dir_path,'tmp_file')
    return tmp_file_path

