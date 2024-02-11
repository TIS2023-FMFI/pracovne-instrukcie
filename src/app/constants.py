from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer

INSTRUCTIONS_DIR = '../../resources/pdf/'
EMPLOYEES_PATH = '../../resources/employees.csv'


def show_notice(self, message: str) -> None:
    warning_dialog = QDialog(self)
    warning_dialog.setWindowFlag(Qt.FramelessWindowHint)
    warning_dialog.setWindowTitle('Varovanie')
    warning_layout = QVBoxLayout()
    warning_label = QLabel(message)
    warning_label.setStyleSheet('font-size: 14pt;')
    warning_layout.addWidget(warning_label)
    warning_dialog.setLayout(warning_layout)
    # Set up a QTimer to close the dialog after 2 seconds
    timer = QTimer(warning_dialog)
    timer.timeout.connect(warning_dialog.accept)  # Close the dialog
    timer.start(2500)  # 2000 milliseconds = 2 seconds

    warning_dialog.exec_()
