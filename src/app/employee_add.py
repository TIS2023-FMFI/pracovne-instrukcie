from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import employees
from csv import writer

from constants import EMPLOYEES_PATH, show_warning


class AddEmployee(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        loadUi('ui/add_employee.ui', self)

        self.add_button.clicked.connect(self.button_add_clicked)
        self.close_button.clicked.connect(self.close_window)

    def button_add_clicked(self) -> None:
        form_names = [self.code.text().strip(), self.last_name.text().strip(), self.first_name.text().strip()]
        if any(form == '' for form in form_names):
            show_warning(self, 'All fields must be filled in!')

        else:
            if employees.employee_exist(self.code.text().strip()):
                show_warning(self, 'Employee with this code already exists')

            else:
                self.close_window()

                with open(EMPLOYEES_PATH, 'a', newline='', encoding='utf-8') as file:
                    writer_object = writer(file)
                    writer_object.writerow(form_names)
                    file.close()

                show_warning(self, 'Employee has been added')

    def close_window(self) -> None:
        self.code.setText('')
        self.last_name.setText('')
        self.first_name.setText('')
        self.close()
