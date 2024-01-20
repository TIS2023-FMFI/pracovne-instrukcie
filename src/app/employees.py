import csv

file_path = '../../resources/employees.csv'


def valid_code(code: str) -> str | bool:
    # TODO:
    #  read_file() save in buffer (unless changed file by admin)
    #  load with start (init)
    employees = read_file()

    if code in employees:
        name = employees[code]
        return name

    else:
        return False


def read_file() -> dict[str, str]:
    employees = dict()

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for line in csvreader:
            code = line[0]
            name = line[2]+ ' ' + line[1]

            employees[code] = name

    return employees
