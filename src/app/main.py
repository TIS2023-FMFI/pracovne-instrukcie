import sys
import os

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel, QPushButton, \
    QToolButton, QSpacerItem

import employees

from pdf_viewer import PDFViewer
from validation import Validation
from histogram import Histogram
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
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)

        # User
        self.username: str = ''
        self.is_admin: bool = False
        self.logout_button.clicked.connect(self.log_out)

        # Instructions
        self.instructions_dir: str = '../../resources/pdf/'
        # TODO: replace with DB query
        self.instructions: dict[int, str] = {
            i: self.instructions_dir + instruction
            for i, instruction in enumerate(os.listdir(self.instructions_dir))
            if instruction.endswith('.pdf')
        }
        self.instruction_names: list[str] = [
            instruction.removesuffix('.pdf')
            for instruction in os.listdir(self.instructions_dir)
            if instruction.endswith('.pdf')
        ]

        # Search Instructions
        self.search_engine: Search = Search(self.instructions_dir)
        self.search_input.textChanged.connect(self.display_instructions)

        # View Instructions
        self.pdf_viewer: PDFViewer = PDFViewer(self)
        self.listWidget.itemClicked.connect(self.clicked)
        self.display_instructions()

        # Validate Instructions
        self.validation_window: Validation = Validation(self.instructions_dir)

        # Histogram
        self.histogram: Histogram = Histogram()
        self.histogram_button.clicked.connect(self.histogram.plot_histogram)

    def display_instructions(self) -> None:
        # TODO: replace with DB query?
        instruction_names: list[str] = self.search_engine.filter_instructions(self.search_input.text())
        self.listWidget.clear()

        for i, name in enumerate(instruction_names):
            item = QListWidgetItem(name)
            item_widget = QWidget()
            item_widget.setObjectName('button_placeholder')

            button = QPushButton('Validovať')
            button.setObjectName(str(i + 1))
            button.clicked.connect(self.validate)

            item_layout = QHBoxLayout()
            item_layout.addStretch()
            item_layout.addWidget(button)

            item_widget.setLayout(item_layout)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, item_widget)

    def validate(self):
        self.validation_window.hide()
        validation_id = int(self.sender().objectName())

        # TODO: replace with DB query
        self.validation_window.set_file(
            validation_id,
            self.instruction_names[validation_id - 1],
            self.instructions[validation_id - 1]
        )

        self.validation_window.show()

    def log_in(self, username: str, is_admin: bool) -> None:
        self.username = username
        self.is_admin = is_admin
        self.username_label.setText(username)

    def log_out(self) -> None:
        self.username_label.setText('')
        self.search_input.setText('')
        self.pdf_viewer.hide()
        self.validation_window.hide()
        self.histogram.hide()

        self.display_instructions()

        self.login_window.showFullScreen()
        self.hide()

    def clicked(self, item: str) -> None:
        self.open_instruction(item.text())

    def open_instruction(self, file_name: str) -> None:
        name: str = file_name
        path = self.instructions_dir + file_name + '.pdf'
        self.pdf_viewer.set_document(path, name)
        self.pdf_viewer.display()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = MainWindow()
    app.exec()
