from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel

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
            self.show_message()
        else:
            self.hide()

            code = self.code.text()
            self.code.setText('')
            with open(self.employees_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)

            rows = [row for row in rows if row[0] != code]

            with open(self.employees_file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)


    def show_message(self):
        warning_dialog = QDialog(self)
        warning_dialog.setWindowTitle("Notice")
        warning_layout = QVBoxLayout()
        warning_label = QLabel("All fields must be filled in!")
        warning_layout.addWidget(warning_label)
        warning_dialog.setLayout(warning_layout)
        warning_dialog.exec_()

    def close_window(self) -> None:
        self.code.setText('')
        self.close()
