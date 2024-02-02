from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from csv import writer

from constants import EMPLOYEES_PATH


class AddEmployee(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        loadUi('ui/add_employee.ui', self)
        self.setStyleSheet(open('ui/add_employee.css').read())

        self.employees_file_path = '../../resources/employees.csv'

        self.add_button.clicked.connect(self.button_add_clicked)
        self.close_button.clicked.connect(self.close_window)

    def show_window(self) -> None:
        self.show()

    def button_add_clicked(self) -> None:
        form_names = [self.code.text().strip(), self.last_name.text().strip(), self.first_name.text().strip()]
        if any(form == '' for form in form_names):
            # TODO: let the user know
            ...

        else:
            self.hide()

            with open(EMPLOYEES_PATH, 'a', newline='', encoding='utf-8') as file:
                writer_object = writer(file)
                writer_object.writerow(form_names)
                file.close()

    def close_window(self) -> None:
        self.code.setText('')
        self.last_name.setText('')
        self.first_name.setText('')
        self.close()
