import sys
import os
import shutil

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QFileDialog

import datetime
from dateutil.relativedelta import relativedelta
from database_manager import DBManager
from PyQt5.QtCore import pyqtSignal

from constants import INSTRUCTIONS_DIR, show_notice


class InstructionValidate(QWidget):
    signal: pyqtSignal = pyqtSignal()

    def __init__(self) -> None:
        QWidget.__init__(self)
        loadUi("ui/validation.ui", self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.close_button.clicked.connect(self.close_validation)
        self.select_button.clicked.connect(self.select_file)
        self.validate_button.clicked.connect(self.validate)

        self.frequency_combobox.addItems([str(i) for i in range(1, 13)])

        self.database = DBManager()

        self.selectedFilePath: str = ''
        self.file_path: str = ''
        self.file_name: str = ''
        self.id: int = 0

    def select_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select file", INSTRUCTIONS_DIR, "PDF files (*.pdf)")
        self.selectedFilePath = path
        self.path_label.setText(path.split("/")[-1])

    def set_file(self, _id, name, path) -> None:
        self.file_path: str = path
        self.file_name: str = name
        self.id: int = _id
        self.instruction_name.setText(name)

    def close_validation(self):
        self.path_label.setText('')
        self.close()

    def validate(self) -> None:
        new_instruction = self.path_label.text()
        frequency = int(self.frequency_combobox.currentText())
        today = datetime.datetime.today()
        expiration = today + relativedelta(months=+frequency)
        expiration_date = expiration.date()
        update_query = f"UPDATE instructions SET "

        if new_instruction:
            update_query += f"file_path='{INSTRUCTIONS_DIR + new_instruction}', "
            if self.selectedFilePath:
                try:
                    shutil.copy2(self.selectedFilePath, INSTRUCTIONS_DIR)
                    os.remove(self.file_path)

                except Exception as e:
                    print(f"Error copying/removing file: {e}")

            else:
                print('error')
                return

        update_query += f"validation_date=CURRENT_DATE, expiration_date='{expiration_date}' WHERE id={self.id}"
        self.database.execute_query(update_query)
        self.database.execute_query(f"INSERT INTO validations (instruction_id) VALUES ('{self.id}')")

        print(self.database.execute_query(f"SELECT * FROM instructions WHERE id = {self.id}"))
        self.signal.emit()

        show_notice(self, 'Inštrukcia bola validovaná')
        self.close_validation()
