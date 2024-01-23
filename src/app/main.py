import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
from pdf_viewer import PDFViewer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QLineEdit

import employees
from keyword_search import Search


class LoginWindow(QDialog):
    def __init__(self) -> None:
        super(LoginWindow, self).__init__()
        loadUi('ui/login.ui', self)

        self.employee_name = ''
        self.login_button.clicked.connect(self.log_in)

        self.showFullScreen()
        self.main_window = MainWindow(self)

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
        self.search_input.textChanged.connect(self.display_instructions)

        self.instructions_dir: str = '../../resources/pdf/'

        self.search_engine: Search = Search(self.instructions_dir)
        self.listWidget.itemClicked.connect(self.clicked)
        self.pdf_viewer: PDFViewer = PDFViewer(self)
        self.display_instructions()

    def display_instructions(self):
        instruction_names: list[str] = self.search_engine.filter_instructions(self.search_input.text())

        self.listWidget.clear()

        for name in instruction_names:
            item = QListWidgetItem(name)
            item.setTextAlignment(Qt.AlignLeft)
            self.listWidget.addItem(item)

    def log_out(self) -> None:
        self.search_input.setText('')
        self.display_instructions()

        self.pdf_viewer.hide()
        self.hide()
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
