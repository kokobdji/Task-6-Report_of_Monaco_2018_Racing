import argparse
from unittest.mock import patch

import pytest

from reporter.reader import main, parse


@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(files=None))
def test_files_error(mock_args_parse):
    with pytest.raises(Exception) as ExceptionInfo:
        parse()
        assert 'the following arguments are required: --files' == str(ExceptionInfo.value)
        mock_args_parse.assert_called_once()


@patch('argparse.ArgumentParser.parse_args',
       return_value=argparse.Namespace(files='C://', driver='Il gatto'))
def test_parse_positive(mock_args_parse):
    assert parse() == argparse.Namespace(files='C://', driver='Il gatto')
    mock_args_parse.assert_called_once()


@patch('reporter.reader.files_path_check', return_value='not_existing_dir.wow')
@patch('reporter.report.Reporter.build_reporter')
@patch('reporter.report.Reporter.driver_info', return_value='Il gatto')
def test_main_driver(mock_driver_info, mock_class, mock_file_path):
    args = argparse.Namespace(files='not_existing_dir.wow', driver='Il gatto', desc=True)
    assert main(args) == 'Il gatto'
    mock_class.assert_called_once()
    mock_driver_info.assert_called_once()
    mock_file_path.assert_called_once()


@patch('reporter.reader.files_path_check', return_value='not_existing_dir.wow')
@patch('reporter.report.Reporter.build_reporter')
@patch('reporter.report.Reporter.driver_info', return_value=None)
def test_main_driver_none(mock_driver_info, mock_class, mock_file_path):
    args = argparse.Namespace(files='not_existing_dir.wow', driver='Il gatto', desc=True)
    assert main(args) == 'Driver not found'
    mock_class.assert_called_once()
    mock_driver_info.assert_called_once()
    mock_file_path.assert_called_once()


@patch('reporter.reader.files_path_check', return_value='not_existing_dir.wow')
@patch('reporter.report.Reporter.build_reporter')
@patch('reporter.report.Reporter.printer', return_value='Giorgio is a driver')
def test_main_printer(mock_printer, mock_class, mock_file_path):
    args = argparse.Namespace(files='not_existing_dir.wow', driver=None, desc=True)
    assert main(args) == 'Giorgio is a driver'
    mock_class.assert_called_with()
    mock_printer.assert_called_once()
    mock_file_path.assert_called_once()
