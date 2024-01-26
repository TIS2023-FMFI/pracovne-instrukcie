import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from pdf_viewer import PDFViewer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QLineEdit

import employees
from keyword_search import Search


class LoginWindow(QDialog):
    def __init__(self, main_window) -> None:
        self.main_window = main_window

        super(LoginWindow, self).__init__()
        loadUi('ui/login.ui', self)

        self.login_button.clicked.connect(self.log_in)

    def log_in(self) -> None:
        password_input: str = str(self.login_input.text())
        username: str = employees.get_username(password_input)
        isAdmin: bool = employees.verify_admin(password_input)

        if isAdmin:
            username = 'Admin'

        if username is not None:
            self.login_input.setText('')
            self.main_window.log_in(username, isAdmin)

            self.main_window.showFullScreen()
            self.hide()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        self.login_window: QDialog = LoginWindow(self)
        self.login_window.showFullScreen()

        self.username: str = ''
        self.is_admin: bool = False

        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)

        self.logout_button.clicked.connect(self.log_out)
        self.add_employee_button.clicked.connect(self.add_employee_window)
        self.search_input.textChanged.connect(self.display_instructions)

        self.instructions_dir: str = '../../resources/pdf/'

        self.listWidget.itemClicked.connect(self.clicked)
        self.search_engine: Search = Search(self.instructions_dir)
        self.pdf_viewer: PDFViewer = PDFViewer(self)
        self.display_instructions()

    def display_instructions(self):
        instruction_names: list[str] = self.search_engine.filter_instructions(self.search_input.text())

        self.listWidget.clear()

        for name in instruction_names:
            item = QListWidgetItem(name)
            item.setTextAlignment(Qt.AlignLeft)
            self.listWidget.addItem(item)

    def log_in(self, username, is_admin):
        self.username = username
        self.is_admin = is_admin
        self.username_label.setText(username)

    def log_out(self) -> None:
        self.search_input.setText('')
        self.username_label.setText('')
        self.display_instructions()

        self.pdf_viewer.hide()
        self.login_window.showFullScreen()
        self.hide()

    def clicked(self, item) -> None:
        self.open_instruction(item.text())

    def open_instruction(self, file_name) -> None:
        # get display name from file name dict
        name: str = file_name
        self.pdf_viewer.set_document(self.instructions_dir + file_name + '.pdf', name)
        self.pdf_viewer.display()

    def add_employee_window(self):
        new_window = QDialog(self)
        new_window.setWindowTitle('Add employee')

        code = QLineEdit(new_window)
        code.setObjectName('code')
        name = QLineEdit(new_window)
        name.setObjectName('name')
        button_add = QPushButton('Add employee', new_window)
        new_window_layout = QVBoxLayout()
        new_window_layout.addWidget(QLabel('code:', new_window))
        new_window_layout.addWidget(code)
        new_window_layout.addWidget(QLabel('name:', new_window))
        new_window_layout.addWidget(name)
        new_window_layout.addWidget(button_add)
        new_window.setLayout(new_window_layout)

        button_add.clicked.connect(self.on_ok_button_clicked)
        new_window.exec_()

    def on_ok_button_clicked(self):
        sender_button = self.sender()
        new_window = sender_button.parent()
        code = new_window.findChild(QLineEdit, 'code')
        name = new_window.findChild(QLineEdit, 'name')

        if code.text().strip() == '' or name.text().strip() == '':
            QMessageBox.warning(new_window, 'Missing data', 'All fields must be filled in.')
        else:
            employees.add_employee(code.text(), name.text())
            new_window.accept()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = MainWindow()
    app.exec()
