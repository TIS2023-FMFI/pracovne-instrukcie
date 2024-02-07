import os

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal

from database_manager import DBManager


class InstructionDelete(QWidget):
    signal: pyqtSignal = pyqtSignal()

    def __init__(self) -> None:
        QWidget.__init__(self)
        loadUi("ui/confirmation_window.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.database: DBManager = DBManager()
        self.file_path = None

        self.accept_button.clicked.connect(self.confirm)
        self.reject_button.clicked.connect(self.close)

        self.instruction_id: int = 0

    def confirm(self) -> None:
        self.delete_instruction()
        self.signal.emit()
        self.close()

    def set_title(self, name) -> None:
        text: str = "Vymazať " + name + " ?"
        self.title.setText(text)

    def confirmation(self, instruction_id) -> None:
        self.hide()
        self.instruction_id = instruction_id
        title, self.file_path = self.database.execute_query(f"SELECT name, file_path FROM instructions WHERE id = {instruction_id}")[0]
        self.set_title(title)
        self.show()

    def delete_instruction(self) -> None:
        self.database.execute_query(f"DELETE FROM instructions WHERE id = {self.instruction_id}")
        os.remove(self.file_path)
        self.instruction_id = 0
        self.signal.emit()
