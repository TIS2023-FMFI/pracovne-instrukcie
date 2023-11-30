import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel


class LoginWindow(QDialog):
    def __init__(self) -> None:
        super(LoginWindow, self).__init__()
        loadUi('ui/login.ui', self)
        self.main_window = MainWindow(self)

        self.login_button.clicked.connect(self.log_in)
        self.showFullScreen()

    def log_in(self) -> None:
        # TODO: login logistics
        self.main_window.showFullScreen()
        self.hide()


class MainWindow(QMainWindow):
    def __init__(self, login_window) -> None:
        self.login_window: QDialog = login_window
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)

        self.logout_button.clicked.connect(self.log_out)

        self.instructions = [ "../../resources/pdf/" + instruction for instruction in os.listdir( "../../resources/pdf" ) if instruction.endswith( ".pdf" ) ]
        print( self.instructions )
        self.display_instructions()
        


    def log_out(self) -> None:
        self.hide()
        self.login_window.showFullScreen()

    def display_instructions( self ) -> None:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = LoginWindow()
    app.exec()
