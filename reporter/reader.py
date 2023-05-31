import argparse
from argparse import Namespace

from .report import Driver, Reporter
from .utils import driver_name_check, files_path_check


def parse() -> Namespace:
    parser = argparse.ArgumentParser(
        prog='CollectionFramework',
        description='Read data from 2 files, order racers by '
                    'time and print report that shows '
                    'the top 15 racers and the rest after underline')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--asc', action='store_true')
    group.add_argument('--desc', action='store_true', help='sorted by', default=False)
    parser.add_argument('--files', help='Enter your logs path', required=True)
    parser.add_argument('--driver', required=False)
    args = parser.parse_args()
    return args


def main(args: Namespace) -> Driver | str:
    info = Reporter(files_path_check(args.files), args.desc)
    if args.driver:
        message = info.driver_info(driver_name_check(args.driver))
        if message is None:
            return 'Driver not found'
        return message
    return info.printer()
