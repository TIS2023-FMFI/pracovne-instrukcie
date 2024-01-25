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
        self.instructions_dir: str = '../../resources/pdf/'

        #TODO: replace with DB query
        self.instructions: dict[int,str] = {
            id : self.instructions_dir + instruction
            for id, instruction in enumerate(os.listdir(self.instructions_dir)) if instruction.endswith('.pdf')
        }
        self.instruction_names: list[str] = [
            instruction.removesuffix('.pdf')
            for instruction in os.listdir(self.instructions_dir) if instruction.endswith('.pdf')
        ]
        
        self.pdf_viewer: PDFViewer = PDFViewer(self)
        self.validation_window = Validation( self.instructions_dir )
        self.histogram = Histogram()
        self.logout_button.clicked.connect(self.log_out)
        self.histogram_button.clicked.connect( self.histogram.plot_histogram )
        self.listWidget.itemClicked.connect(self.clicked)

        self.display_instructions()

    def display_instructions(self):
        #TODO: replace with DB query
        for id, name in enumerate(self.instruction_names):
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

    def log_out(self) -> None:
        self.hide()
        self.validation_window.hide()
        self.pdf_viewer.hide()
        self.login_window.showFullScreen()

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
    w = LoginWindow()
    app.exec()
