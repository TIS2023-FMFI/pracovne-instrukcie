import sys
import os

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel, QPushButton,\
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

        self.username: str = ''
        self.is_admin: bool = False

        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)

        #TODO: replace with DB query
        self.instructions: dict[int,str] = {
            id : self.instructions_dir + instruction
            for id, instruction in enumerate(os.listdir(self.instructions_dir)) if instruction.endswith('.pdf')
        }
        self.instruction_names: list[str] = [
            instruction.removesuffix('.pdf')
            for instruction in os.listdir(self.instructions_dir) if instruction.endswith('.pdf')
        ]
        
        self.logout_button.clicked.connect(self.log_out)
        self.search_input.textChanged.connect(self.display_instructions)

        self.instructions_dir: str = '../../resources/pdf/'

        self.listWidget.itemClicked.connect(self.clicked)
        self.search_engine: Search = Search(self.instructions_dir)

        self.pdf_viewer: PDFViewer = PDFViewer(self)
        self.validation_window = Validation( self.instructions_dir )
        self.histogram = Histogram()
        self.logout_button.clicked.connect(self.log_out)
        self.histogram_button.clicked.connect( self.histogram.plot_histogram )
        self.listWidget.itemClicked.connect(self.clicked)

        self.display_instructions()

    def display_instructions(self):

        #TODO: replace with DB query?
        instruction_names: list[str] = self.search_engine.filter_instructions(self.search_input.text())
        self.listWidget.clear()
        for id, name in enumerate(instruction_names):
            item = QListWidgetItem(name)
            item_widget = QWidget()
            item_widget.setObjectName("button_placeholder")

            button = QPushButton("Validovať")
            button.setObjectName(str(id + 1))
            button.clicked.connect(self.validate)

            item_layout = QHBoxLayout()
            item_layout.addStretch()
            item_layout.addWidget(button)
            
            item_widget.setLayout(item_layout)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, item_widget)


    def validate(self):
        self.validation_window.hide()
        id = int(self.sender().objectName())

        #TODO: replace with DB query
        self.validation_window.set_file(id, self.instruction_names[id -1], self.instructions[id -1])
        self.validation_window.show()

    def log_in(self, username, is_admin):
        self.username = username
        self.is_admin = is_admin
        self.username_label.setText(username)

    def log_out(self) -> None:
        self.validation_window.hide()
        self.search_input.setText('')
        self.username_label.setText('')
        self.display_instructions()

        self.pdf_viewer.hide()
        self.login_window.showFullScreen()
        self.hide()

    def clicked(self, item) -> None:
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
