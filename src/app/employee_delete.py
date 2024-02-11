from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import csv
import employees

from constants import EMPLOYEES_PATH, show_notice


class DeleteEmployee(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        loadUi('ui/delete_employee.ui', self)

        self.delete_button.clicked.connect(self.delete_add_clicked)
        self.close_button.clicked.connect(self.close_window)

    def delete_add_clicked(self) -> None:
        if self.code.text().strip() == '':
            show_notice(self, 'Všetky povinné polia musia byť vyplnené')

        else:
            code = self.code.text()
            if employees.employee_exist(code):
                with open(EMPLOYEES_PATH, 'r', newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    rows = list(csv_reader)

                rows = [row for row in rows if row[0] != code]

                with open(EMPLOYEES_PATH, 'w', newline='', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)

                show_notice(self, 'Zamestnanec bol odstránený')
                self.close_window()

            else:
                show_notice(self, 'Zamestnanec so zadaným kódom neexistuje')

    def close_window(self) -> None:
        self.code.setText('')
        self.close()
