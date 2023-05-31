from unittest.mock import mock_open, patch

import pytest

from reporter.exceptions import NotFound
from reporter.utils import driver_name_check, files_path_check, open_file


@patch('os.path.exists', return_value=False)
def test_path_error_positive(mock_exists):
    with pytest.raises(NotFound) as ExceptionInfo:
        files_path_check(mock_exists)
        assert 'Not found directory' == str(ExceptionInfo.value)
        mock_exists.assert_called_once()


@patch('os.path.exists', return_value=True)
@pytest.mark.parametrize('direction', ['/my_files'])
def test_path(mock_exists, direction):
    assert files_path_check(direction) == '/my_files'
    mock_exists.assert_called_once()


@pytest.mark.parametrize('name', ['123456', 'Giorgio Novozhylov!', '!!!Andrii Divnych!!!'])
def test_name_error(name):
    with pytest.raises(Exception) as ExceptionInfo:
        driver_name_check(name)
    assert 'Name of driver contains numbers or symbols' == str(ExceptionInfo.value)


@pytest.mark.parametrize('name', ['Giorgio Novozhylov  ', '  Andrii Dyvnich'])
def test_name_positive(name):
    assert driver_name_check(name) == name.strip()


@patch('builtins.open', new_callable=mock_open, read_data='data')
def test_file_reading(mock_file):
    assert open_file("path/to/open") == ["data"]
    mock_file.assert_called_once()
