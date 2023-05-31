import datetime
import os
from dataclasses import dataclass
from typing import Optional

from .constants import ABBREVIATIONS, END, NAME_SLICE, START, TIME_FORMATTER, TIME_FORMATTER_SLICE, TIME_SLICE
from .utils import open_file


@dataclass
class Driver:
    name: str
    team: str
    abbv: str
    time: str

    def __repr__(self):
        return f'{self.name}   |   {self.team}   |   {self.time}'


class Reporter:
    def __init__(self, location: str, order_by: bool):
        self.location = location
        self.order_by = order_by
        self.driver_list: list[Driver] = self.build_reporter()

    def build_reporter(self) -> list[Driver]:
        start_time_data = open_file(os.path.join(self.location, START))
        end_time_data = open_file(os.path.join(self.location, END))
        names_data = open_file(os.path.join(self.location, ABBREVIATIONS))
        sorted_start_time = self.time_file_formatter(start_time_data)
        sorted_end_time = self.time_file_formatter(end_time_data)
        time_result: dict = self.time_counter(sorted_start_time, sorted_end_time)
        driver_list: list[Driver] = []
        for name, time in time_result.items():
            data_names = self.name_file_formatter(names_data)
            if name in data_names:
                driver_list.append(Driver(name=data_names[name][0],
                                          team=data_names[name][1],
                                          abbv=name,
                                          time=time))
        return driver_list

    @staticmethod
    def name_file_formatter(names_data: list) -> dict:
        driver_names = {}
        for info in names_data:
            if not info.isspace():
                data = info.rstrip().split('_')
                driver_names[data[0]] = data[NAME_SLICE]
        return driver_names

    @staticmethod
    def time_file_formatter(log_data: list) -> dict:
        time = {}
        for time_info in log_data:
            if not time_info.isspace():
                data = time_info.rstrip().split('_')
                time[data[0][TIME_FORMATTER_SLICE]] = datetime.datetime.strptime(data[-1], TIME_FORMATTER)
        return time

    @staticmethod
    def time_counter(sorted_start_time: dict, sorted_end_time: dict) -> dict:
        time_result = {}
        for name in sorted_end_time:
            if name in sorted_start_time:
                delta = sorted_end_time[name] - sorted_start_time[name]
                if delta.days < 0:
                    time_result[name] = 'Time error'
                else:
                    time_result[name] = str(delta)[TIME_SLICE]
        return time_result

    def driver_sorting(self) -> list[Driver]:
        return sorted(self.driver_list, key=lambda x: x.time, reverse=self.order_by)

    def rank_message(self) -> list[str]:
        message = []
        flag = True
        for num, info in enumerate(self.driver_sorting(), 1):
            if self.order_by is False:
                if info.time == 'Time error' and flag is True:
                    message.append('-' * 50)
                    flag = False
                message.append(f'{num}|   {info}')
            else:
                if info.time != 'Time error' and flag is True:
                    message.append('-' * 50)
                    flag = False
                message.append(f'{num}|   {info}')
        return message

    def printer(self) -> str:
        return '\n'.join(self.rank_message())

    def driver_info(self, driver_name) -> Optional[Driver]:
        for driver in self.driver_list:
            if driver_name == driver.name:
                return driver
        return None
