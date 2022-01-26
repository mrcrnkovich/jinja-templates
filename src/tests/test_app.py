""" Setup Pytest """

import subprocess
from unittest.mock import MagicMock
import app


def test_dir_exists(tmp_path):
    """ Confirms that if a directory exists the app returns the existing
        directory
    """

    tmp_file = tmp_path / "test_dir"
    tmp_file.mkdir()

    assert app.dir_exists(tmp_file) == tmp_file


def test_check_dependencies():
    """ sets the subprocess call to True or False to
        Check whenever check_dependencies returns
        the appropriate boolean based on the system's
        return value
    """
    subprocess.call = MagicMock(return_value=1)
    assert app.check_dependencies() is True

    subprocess.call = MagicMock(return_value=0)
    assert app.check_dependencies() is False
