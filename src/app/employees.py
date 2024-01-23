import csv
import configparser

file_path = '../../resources/employees.csv'


def verify_admin(code: str) -> bool:
    config: configparser = configparser.ConfigParser()
    config.read('config.ini')
    if code == config.get('Admin', 'password'):
        return True

    return False


def get_username(code: str) -> str | None:
    # TODO:
    #  read_file() save in buffer (unless changed file by admin)
    #  load with start (init)
    employees = read_file()

    if code in employees:
        name = employees[code]
        return name

    return None


def read_file() -> dict[str, str]:
    employees = dict()

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for line in csvreader:
            code = line[0]
            name = line[2] + ' ' + line[1]

            employees[code] = name

    return employees
