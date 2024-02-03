from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import csv


class DeleteEmployee(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        loadUi('ui/delete_employee.ui', self)
        self.setStyleSheet(open('ui/add_employee.css').read())

        self.employees_file_path = '../../resources/employees.csv'

        self.delete_button.clicked.connect(self.delete_add_clicked)
        self.close_button.clicked.connect(self.close_window)

    def show_window(self) -> None:
        self.show()

    def delete_add_clicked(self) -> None:
        if self.code.text().strip() == '':
            ...
        else:
            self.hide()

            code = self.code.text()
            with open(self.employees_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)

            rows = [row for row in rows if row[0] != code]

            with open(self.employees_file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)


    def close_window(self) -> None:
        self.code.setText('')
        self.close()
