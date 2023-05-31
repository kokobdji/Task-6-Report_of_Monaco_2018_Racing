import os

from reporter.exceptions import NotFound, SymbolMistakes


def open_file(file_folder) -> list:
    with open(file_folder, 'r', encoding='utf-8') as log_file:
        return log_file.readlines()


def files_path_check(path: str) -> str:
    if not os.path.exists(path):
        raise NotFound('Not found directory')
    return path


def driver_name_check(name: str) -> str:
    if not ''.join(name.split()).isalpha():
        raise SymbolMistakes('Name of driver contains numbers or symbols')
    return name.strip().title()
