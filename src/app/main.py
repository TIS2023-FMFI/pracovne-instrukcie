import sys

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QLineEdit

import employees

first_name_of_employee = ""
last_name_of_employee = ""


class LoginWindow(QDialog):
    def __init__(self) -> None:
        super(LoginWindow, self).__init__()
        loadUi('ui/login.ui', self)
        self.main_window = MainWindow(self)

        self.login_button.clicked.connect(self.log_in)
        self.showFullScreen()


    def log_in(self) -> None:
        code = str(self.login_input.text())
        log_data = employees.valid_code(code)

        if log_data != False:
            first_name_of_employee = log_data[1]
            last_name_of_employee = log_data[2]
            self.main_window.showFullScreen()
            self.hide()


class MainWindow(QMainWindow):
    def __init__(self, login_window) -> None:
        self.login_window: QDialog = login_window
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)

        self.logout_button.clicked.connect(self.log_out)

    def log_out(self) -> None:
        first_name_of_employee = ""
        last_name_of_employee = ""
        self.hide()
        self.login_window.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = LoginWindow()
    app.exec()
