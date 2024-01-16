import csv

file_path = '../../resources/employees.csv'
employees = {}

def get_employee_first_name(code: str) -> str:
    return employees.get(code, {}).get('first_name')
def get_employee_last_name(code: str) -> str:
    return employees.get(code, {}).get('last_name')

def valid_code(code: str):
    read_file()
    if code in employees:
        first_name = get_employee_first_name(code)
        last_name = get_employee_last_name(code)
        return True, first_name, last_name
    else:
        return False

def read_file():
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        for line in csvreader:
            line_without_commas = [sign.replace(',', '') for sign in line]
            code = str(line_without_commas[0])
            first_name = str(line_without_commas[2])
            last_name = str(line_without_commas[1])

            employees[code] = {'first_name': first_name, 'last_name': last_name}

