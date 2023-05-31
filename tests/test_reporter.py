import datetime
from unittest.mock import MagicMock, patch

import pytest

from reporter.report import Driver, Reporter


@pytest.mark.parametrize('input_data, expected', [(['DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\n'],
                                                   {'DRR': ['Daniel Ricciardo', 'RED BULL RACING TAG HEUER']})])
def test_name_sort(input_data, expected):
    assert Reporter.name_file_formatter(input_data) == expected


@pytest.mark.parametrize('input_data, expected', [(['SVF2018-05-24_12:02:58.917\n'],
                                                   {'SVF': datetime.datetime(1900, 1, 1, 12, 2, 58, 917000)})])
def test_time_format(input_data, expected):
    assert Reporter.time_file_formatter(input_data) == expected


@pytest.mark.parametrize('input_data_start, input_data_end, expected',
                         [({'SVF': datetime.datetime(1900, 1, 1, 12, 2, 58, 917000)},
                           {'SVF': datetime.datetime(1900, 1, 1, 12, 4, 3, 332000)},
                           {'SVF': '1:04.415'}),
                          ({'DRR': datetime.datetime(1900, 1, 1, 12, 14, 12, 54000)},
                           {'DRR': datetime.datetime(1900, 1, 1, 12, 11, 24, 67000)},
                           {'DRR': 'Time error'})])
def test_time_counter(input_data_start, input_data_end, expected):
    assert Reporter.time_counter(input_data_start, input_data_end) == expected


@pytest.mark.parametrize('input_list, expected, order',
                         [([Driver(name='Giorgio', team='Juv', time='1', abbv='GJ'),
                            Driver(name='Andrii', team='Juv', time='2', abbv='AJ')],
                           [Driver(name='Giorgio', team='Juv', time='1', abbv='GJ'),
                            Driver(name='Andrii', team='Juv', time='2', abbv='AJ')],
                           False),
                          ([Driver(name='Giorgio', team='Juv', time='1', abbv='GJ'),
                            Driver(name='Andrii', team='Juv', time='2', abbv='AJ')],
                           [Driver(name='Andrii', team='Juv', time='2', abbv='AJ'),
                            Driver(name='Giorgio', team='Juv', time='1', abbv='GJ')],
                           True)])
def test_driver_sorting(input_list, expected, order):
    mock_class = MagicMock()
    mock_class.order_by = order
    mock_class.driver_list = input_list
    assert Reporter.driver_sorting(mock_class) == expected


@pytest.mark.parametrize('input_lists, expected',
                         [(['Some information about drivers'],
                           'Some information about drivers')])
def test_printer(input_lists, expected):
    with patch.object(Reporter, 'rank_message', return_value=input_lists) as mock_method:
        mock_class = Reporter
        assert Reporter.printer(mock_class) == expected


@pytest.mark.parametrize('driver_list, driver_name, expected',
                         [([Driver(name='Giorgio', team='Juv', time='1', abbv='GJ')],
                           'Giorgio', Driver(name='Giorgio', team='Juv', time='1', abbv='GJ')),
                          ([Driver(name='Giorgio', team='Juv', time='1', abbv='GJ')],
                           'Andrii', None)])
def test_driver_info(driver_list, driver_name, expected):
    mock_class = MagicMock()
    mock_class.driver_list = driver_list
    assert Reporter.driver_info(mock_class, driver_name) == expected


@pytest.mark.parametrize('driver_list, expected, order',
                         [([Driver(name='Giorgio', team='Juv', time='1', abbv='GJ'),
                            Driver(name='Andrii', team='Juv', time='Time error', abbv='AJ')],
                           ['1|   Giorgio   |   Juv   |   1',
                            '--------------------------------------------------',
                            '2|   Andrii   |   Juv   |   Time error'],
                           False),
                          ([Driver(name='Giorgio', team='Juv', time='Time error', abbv='GJ'),
                            Driver(name='Andrii', team='Juv', time='1', abbv='AJ')],
                           ['1|   Giorgio   |   Juv   |   Time error',
                            '--------------------------------------------------',
                            '2|   Andrii   |   Juv   |   1'],
                           True)])
def test_rank_message(driver_list, expected, order):
    with patch.object(Reporter, 'driver_sorting', return_value=driver_list) as mock_driver_sort:
        mock_class = Reporter
        mock_class.order_by = order
        assert Reporter.rank_message(mock_class) == expected


def data_maker(name_of_file):
    if name_of_file.endswith('start.log'):
        return ['SVF2018-05-24_12:02:58.917\n', 'NHR2018-05-24_12:02:49.914\n']
    elif name_of_file.endswith('end.log'):
        return ['SVF2018-05-24_12:04:03.332\n', 'NHR2018-05-24_12:04:02.979\n']
    else:
        return ['SVF_Sebastian Vettel_FERRARI\n', 'NHR_Nico Hulkenberg_RENAULT\n']


@patch('reporter.report.open_file')
def test_build_reporter(mock_open_file):
    mock_open_file.side_effect = data_maker
    driver_list = Reporter('some_path', True).build_reporter()
    assert isinstance(driver_list, list)
    for driver in driver_list:
        assert isinstance(driver, Driver)
    mock_open_file.assert_called()
