from unittest.mock import MagicMock
import app
import subprocess


def test_dir_exists(tmp_path):
    tmp_file = tmp_path / "test_dir"
    tmp_file.mkdir()

    assert app.dir_exists(tmp_file) == tmp_file


def test_check_dependencies():

    subprocess.call = MagicMock(return_value=1)
    assert app.check_dependencies() == True

    subprocess.call = MagicMock(return_value=0)
    assert app.check_dependencies() == False
