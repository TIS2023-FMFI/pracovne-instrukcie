import sys
import os

from PyQt5 import QtGui
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel, QPushButton, \
    QToolButton, QSpacerItem, QListWidgetItem, QMessageBox

from constants import INSTRUCTIONS_DIR

from database_manager import DBManager

import employees
from add_employee import AddEmployee
from user_history import History

from instruction import Instruction, initialize_instructions
from keyword_search import Search
from instruction_viewer import InstructionViewer
from instruction_validate import InstructionValidate
from histogram import Histogram
from instruction_add import InstructionAdd
from instruction_delete import InstructionDelete


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
            self.main_window.log_in_user(username, isAdmin)

            self.main_window.showFullScreen()
            self.hide()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        self.login_window: QDialog = LoginWindow(self)
        self.login_window.showFullScreen()
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)

        # Database
        self.database: DBManager = DBManager()

        # User
        self.username: str = ''
        self.is_admin: bool = False
        self.history: History = History()
        self.user_history: list[int] = []
        self.logout_button.clicked.connect(self.log_out_user)

        # Add new Employee
        self.add_employee: AddEmployee = AddEmployee()
        self.add_employee_button.clicked.connect(self.add_employee.show_window)

        # Instructions
        self.instructions_DB: list[Instruction] = initialize_instructions()

        # Search Instructions
        self.search_engine: Search = Search()
        self.search_input.textChanged.connect(self.display_instructions)

        # View Instructions
        self.pdf_viewer: InstructionViewer = InstructionViewer()
        self.listWidget.itemClicked.connect(lambda item: self.open_instruction(item.data(Qt.UserRole)))
        self.display_instructions()

        # Validate Instructions
        self.instruction_validate: InstructionValidate = InstructionValidate()
        self.instruction_validate.signal.connect(self.reload_instruction)

        # Histogram
        self.histogram: Histogram = Histogram()
        self.histogram_button.clicked.connect(self.histogram.plot_histogram)

        # Add instruction
        self.instruction_add: InstructionAdd = InstructionAdd()
        self.add_instruction_button.clicked.connect(self.instruction_add.display_window)
        self.instruction_add.signal.connect(self.reload_instruction)

        # Delete Instruction
        self.instruction_delete: InstructionDelete = InstructionDelete()
        self.instruction_delete.signal.connect(self.reload_instruction)

    def log_in_user(self, username: str, is_admin: bool) -> None:
        self.username = username
        self.is_admin = is_admin
        self.username_label.setText(username)

        self.user_history = self.history.get_user_history(self.username)
        self.display_instructions()

    def log_out_user(self) -> None:
        self.username_label.setText('')
        self.search_input.setText('')

        self.pdf_viewer.hide()
        self.instruction_validate.hide()
        self.histogram.hide()
        self.instruction_add.hide()
        self.instruction_delete.hide()

        self.display_instructions()

        self.login_window.showFullScreen()
        self.hide()

    def display_instructions(self) -> None:
        filtered_instructions: list[Instruction] = self.search_engine.filter_instructions(self.search_input.text(),
                                                                                          tuple(self.user_history),
                                                                                          self.instructions_DB)

        self.listWidget.clear()
        for instruction in filtered_instructions:
            item = QListWidgetItem(instruction.name)
            item.setData(Qt.UserRole, instruction)
            item_widget = QWidget()
            item_widget.setObjectName('button_placeholder')

            button = QPushButton('Validovať')
            button.setProperty('Instruction', instruction)
            button.clicked.connect(self.validate_instruction)

            button2 = QPushButton("Vymazať")
            button2.setStyleSheet("QPushButton{ background-color: red;}")
            button2.setProperty('Instruction', instruction)
            button2.clicked.connect(self.delete)

            item_layout = QHBoxLayout()
            item_layout.addStretch()
            item_layout.addWidget(button)
            item_layout.addWidget(button2)

            item_widget.setLayout(item_layout)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, item_widget)

    def open_instruction(self, instruction: Instruction) -> None:
        path = INSTRUCTIONS_DIR + instruction.file_path
        self.pdf_viewer.set_document(path, instruction.name)
        self.pdf_viewer.display()
        self.history.log_open_instruction(self.username, instruction.id)

    def validate_instruction(self):
        self.instruction_validate.hide()
        instruction: Instruction = self.sender().property('Instruction')

        self.instruction_validate.set_file(
            instruction.id,
            instruction.name,
            instruction.file_path
        )
        self.instruction_validate.show()

    def delete(self) -> None:
        instruction_id: int = self.sender().property('Instruction').id
        self.instruction_delete.confirmation(instruction_id)

    def reload_instruction(self):
        self.instructions_DB: list[Instruction] = initialize_instructions()
        self.display_instructions()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = MainWindow()
    app.exec()
