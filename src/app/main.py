import sys
from PyQt5.QtWidgets import QApplication
from interface.pyqt.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()  # Initialize your main window
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
