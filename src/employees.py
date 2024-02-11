import csv
import configparser

from typing import Union
from constants import EMPLOYEES_PATH


def verify_admin(code: str) -> bool:
    config: configparser = configparser.ConfigParser()
    config.read('config.ini')
    if code == config.get('Admin', 'password'):
        return True

    return False


def get_username(code: str) -> Union[str, None]:
    employees = read_file()

    if code in employees:
        name = employees[code]
        return name

    return None


def employee_exist(code: str) -> bool:
    codes = read_file()
    if code in codes.keys():
        return True

    return False


def read_file() -> dict[str, str]:
    employees = dict()

    with open(EMPLOYEES_PATH, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for line in csvreader:
            code = line[0]
            name = line[2] + ' ' + line[1]

            employees[code] = name

    return employees
