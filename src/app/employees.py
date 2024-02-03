import csv
import configparser
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

file_path = '../../resources/employees.csv'


def verify_admin(code: str) -> bool:
    config: configparser = configparser.ConfigParser()
    config.read('config.ini')
    if code == config.get('Admin', 'password'):
        return True

    return False


def get_username(code: str) -> str | None:
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

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for line in csvreader:
            code = line[0]
            name = line[2] + ' ' + line[1]

            employees[code] = name

    return employees


def show_message(self, message: str) -> None:
    warning_dialog = QDialog(self)
    warning_dialog.setWindowTitle("Notice")
    warning_layout = QVBoxLayout()
    warning_label = QLabel(message)
    warning_layout.addWidget(warning_label)
    warning_dialog.setLayout(warning_layout)
    warning_dialog.exec_()
