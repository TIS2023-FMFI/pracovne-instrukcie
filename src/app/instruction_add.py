import sys
import shutil

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog

import datetime
from dateutil.relativedelta import relativedelta

from instruction_delete import InstructionDelete
from database_manager import DBManager


class InstructionAdd(QWidget):
    signal: pyqtSignal = pyqtSignal()

    def __init__(self) -> None:
        QWidget.__init__(self)
        loadUi('ui/add_instruction.ui', self)
        self.setStyleSheet(open('ui/instruction_manager.css').read())
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.pdf_path: str = '../../resources/pdf/'

        self.close_button.clicked.connect(self.close)
        self.database: DBManager = DBManager()

        # self.confirmation_window: InstructionDelete = InstructionDelete()
        # self.confirmation_window.signal.connect(self.delete_instruction)

        self.select_button.clicked.connect(self.select_file)
        self.validation_date.setDate(QDate.currentDate())
        self.add_button.clicked.connect(self.add_instruction)
        self.frequency_combobox.addItems([str(i) for i in range(1, 13)])

        self.instruction_id: int = 0
        self.selectedFilePath: str = ''

    def select_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, 'Select file', self.pdf_path, 'PDF files (*.pdf)')
        self.selectedFilePath = path
        self.path_label.setText(path.split('/')[-1])

    def display_window(self) -> None:
        self.hide()
        self.show()

    def close_window(self) -> None:
        self.clear_form()
        self.close()

    def add_instruction(self) -> None:
        name: str = self.instruction_name.text()
        path: str = self.path_label.text()
        validation_date: QDate = self.validation_date.date()
        frequency: int = int(self.frequency_combobox.currentText())
        if path == '' or name == '':
            return

        validation_date: str = validation_date.toString('yyyy-MM-dd')
        validation_date_converted: datetime = datetime.datetime.strptime(validation_date, '%Y-%m-%d')
        expiration_date = validation_date_converted + relativedelta(months=+frequency)

        if self.selectedFilePath:
            try:
                shutil.copy2(self.selectedFilePath, '../../resources/pdf')

            except Exception as e:
                print(f"Error copying file: {e}")

        else:
            return

        query = (f"INSERT INTO instructions (name, file_path, validation_date, expiration_date) "
                 f"VALUES ('{name}', '{self.pdf_path + path}', '{validation_date}', '{expiration_date.date()}') ")

        self.database.execute_query(query)

        self.signal.emit()
        self.clear_form()
        self.close()

    def clear_form(self) -> None:
        self.validation_date.setDate(QDate.currentDate())
        self.instruction_name.setText('')
        self.path_label.setText('')
        self.frequency_combobox.setCurrentText('1')
