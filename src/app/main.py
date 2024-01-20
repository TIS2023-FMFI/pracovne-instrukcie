import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
from pdf_viewer import PDFViewer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QLineEdit

import employees


class LoginWindow(QDialog):
    def __init__(self) -> None:
        super(LoginWindow, self).__init__()
        loadUi('ui/login.ui', self)
        self.main_window = MainWindow(self)

        self.employee_name = ''

        self.login_button.clicked.connect(self.log_in)
        self.showFullScreen()

    def log_in(self) -> None:
        code = str(self.login_input.text())
        log_data = employees.valid_code(code)

        if log_data:
            self.login_input.setText('')
            self.employee_name = log_data

            self.main_window.showFullScreen()
            self.hide()


class MainWindow(QMainWindow):
    def __init__(self, login_window) -> None:
        self.login_window: QDialog = login_window
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)
        self.logout_button.clicked.connect(self.log_out)

        self.instructions_dir: str = '../../resources/pdf/'

        self.instructions: list[str] = [
            self.instructions_dir + instruction
            for instruction in os.listdir(self.instructions_dir) if instruction.endswith('.pdf')
        ]
        self.instruction_names: list[str] = [
            instruction.removesuffix('.pdf')
            for instruction in os.listdir(self.instructions_dir) if instruction.endswith('.pdf')
        ]
        self.pdf_viewer: PDFViewer = PDFViewer(self)
        self.display_instructions()

    def display_instructions(self):
        self.listWidget.itemClicked.connect(self.clicked)
        for name in self.instruction_names:
            item = QListWidgetItem(name)
            item.setTextAlignment(Qt.AlignLeft)
            self.listWidget.addItem(item)

    def log_out(self) -> None:
        self.hide()
        self.pdf_viewer.hide()
        self.login_window.showFullScreen()

    def clicked(self, item) -> None:
        self.open_instruction(item.text())

    def open_instruction(self, file_name) -> None:
        # get display name from file name dict
        name: str = file_name
        self.pdf_viewer.set_document(self.instructions_dir + file_name + '.pdf', name)
        self.pdf_viewer.display()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = LoginWindow()
    app.exec()
