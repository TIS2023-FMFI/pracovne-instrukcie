from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

INSTRUCTIONS_DIR = '../../resources/pdf/'
EMPLOYEES_PATH = '../../resources/employees.csv'


def show_warning(self, message: str) -> None:
    warning_dialog = QDialog(self)
    warning_dialog.setWindowTitle("Notice")
    warning_layout = QVBoxLayout()
    warning_label = QLabel(message)
    warning_layout.addWidget(warning_label)
    warning_dialog.setLayout(warning_layout)
    warning_dialog.exec_()
