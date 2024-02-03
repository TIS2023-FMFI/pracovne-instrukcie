from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QDialog, QVBoxLayout, QLabel

import employees
from csv import writer


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
            self.show_message("All fields must be filled in!")

        else:
            exist = employees.employee_exist(self.code.text().strip())
            if exist:
                self.show_message("Employee with this code already exists")
            else:
                self.code.setText('')
                self.last_name.setText('')
                self.first_name.setText('')
                self.hide()

                with open(self.employees_file_path, 'a', newline='', encoding='utf-8') as file:
                    writer_object = writer(file)
                    writer_object.writerow(form_names)
                    file.close()

                self.show_message("Employee has been added")


    def show_message(self, message:str) -> None:
        warning_dialog = QDialog(self)
        warning_dialog.setWindowTitle("Notice")
        warning_layout = QVBoxLayout()
        warning_label = QLabel(message)
        warning_layout.addWidget(warning_label)
        warning_dialog.setLayout(warning_layout)
        warning_dialog.exec_()

    def close_window(self) -> None:
        self.code.setText('')
        self.last_name.setText('')
        self.first_name.setText('')
        self.close()
