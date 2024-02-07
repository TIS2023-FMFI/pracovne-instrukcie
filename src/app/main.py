import sys
import os

from PyQt5 import QtGui
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QDate, QThreadPool, QTimer
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel, QPushButton, \
    QToolButton, QSpacerItem, QListWidgetItem, QMessageBox

from constants import INSTRUCTIONS_DIR

from database_manager import DBManager

import send_email
import employees
from employee_add import AddEmployee
from employee_delete import DeleteEmployee
from employee_history import History

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

        # # Email Sender
        # self.threadpool: QThreadPool = QThreadPool()
        # self.threadpool.start(send_email.email_sender)

        # User
        self.username: str = ''
        self.is_admin: bool = False
        self.history: History = History()
        self.user_history: list[int] = []
        self.logout_button.clicked.connect(self.log_out_user)

        # Inactivity Timer
        self.inactivity_timer = QTimer(self)
        self.inactivity_timeout = 5 * 60 * 1000  # 5 minutes
        self.inactivity_timer.timeout.connect(self.log_out_user)

        # Instructions
        self.instructions_DB: list[Instruction] = initialize_instructions()

        # Search Instructions
        self.search_engine: Search = Search()
        self.search_input.textChanged.connect(self.display_instructions)
        self.search_input.textChanged.connect(self.restart_inactivity_timer)

        # View Instructions
        self.pdf_viewer: InstructionViewer = InstructionViewer()
        self.listWidget.itemClicked.connect(lambda item: self.open_instruction(item.data(Qt.UserRole)))
        self.listWidget.itemClicked.connect(self.restart_inactivity_timer)
        self.display_instructions()

        # Add new Employee
        self.add_employee: AddEmployee = AddEmployee()
        self.add_employee_button.clicked.connect(self.add_employee.show)
        self.add_employee_button.clicked.connect(self.restart_inactivity_timer)

        # Histogram
        self.histogram: Histogram = Histogram()
        self.histogram_button.clicked.connect(self.histogram.plot_histogram)
        self.histogram_button.clicked.connect(self.restart_inactivity_timer)

        # Delete Employee
        self.delete_employee: DeleteEmployee = DeleteEmployee()
        self.delete_employee_button.clicked.connect(self.delete_employee.show)
        self.delete_employee_button.clicked.connect(self.restart_inactivity_timer)

        # Add instruction
        self.instruction_add: InstructionAdd = InstructionAdd()
        self.add_instruction_button.clicked.connect(self.instruction_add.show)
        self.add_instruction_button.clicked.connect(self.restart_inactivity_timer)
        self.instruction_add.signal.connect(self.reload_instruction)

        # Validate Instructions
        self.instruction_validate: InstructionValidate = InstructionValidate()
        self.instruction_validate.signal.connect(self.reload_instruction)

        # Delete Instruction
        self.instruction_delete: InstructionDelete = InstructionDelete()
        self.instruction_delete.signal.connect(self.reload_instruction)

    def log_in_user(self, username: str, is_admin: bool) -> None:
        self.username = username
        self.is_admin = is_admin
        self.username_label.setText(username)
        if self.is_admin:
            self.add_employee_button.show()
            self.histogram_button.show()
            self.delete_employee_button.show()
            self.add_instruction_button.show()

        else:
            self.add_employee_button.hide()
            self.histogram_button.hide()
            self.delete_employee_button.hide()
            self.add_instruction_button.hide()
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

        self.user_history = list()

        self.inactivity_timer.stop()
        self.login_window.showFullScreen()
        self.hide()

    def restart_inactivity_timer(self) -> None:
        self.inactivity_timer.stop()
        self.inactivity_timer.start(self.inactivity_timeout)

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
            self.listWidget.addItem(item)

            if self.is_admin:
                button = QPushButton('Validovať')
                button.setProperty('Instruction', instruction)
                button.clicked.connect(self.validate_instruction)

                reject_button = QPushButton("Vymazať")
                reject_button.setObjectName("reject_button")
                reject_button.setProperty('Instruction', instruction)
                reject_button.clicked.connect(self.delete)

                today = QDate.currentDate()
                expiration = QDate.fromString(instruction.expiration_date, "yyyy-MM-dd")

                validation = QLabel('Time left')
                validation.setText(str(today.daysTo(expiration)) + ' D')
                validation.setObjectName("instruction_name")

                item_layout = QHBoxLayout()
                item_layout.addStretch()
                item_layout.addWidget(validation)
                item_layout.addWidget(button)
                item_layout.addWidget(reject_button)
                item_widget.setLayout(item_layout)

                self.listWidget.setItemWidget(item, item_widget)

    def open_instruction(self, instruction: Instruction) -> None:
        path = INSTRUCTIONS_DIR + instruction.file_path
        self.pdf_viewer.set_document(path, instruction.name)
        self.pdf_viewer.display()
        if not self.is_admin:
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
    app.setStyleSheet(open('ui/main.css').read())
    w = MainWindow()
    app.exec()
