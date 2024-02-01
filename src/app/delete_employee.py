from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from csv import writer


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

            print(self.code.text())


    def close_window(self) -> None:
        self.code.setText('')
        self.close()
