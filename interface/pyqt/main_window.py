import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path_absolute = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'main_window.ui'))

        try:
            loadUi(ui_path_absolute, self)
        except Exception as e:
            print(f"Error loading UI file: {e}")

        # self.showFullScreen()
