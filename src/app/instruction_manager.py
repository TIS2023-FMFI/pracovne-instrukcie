from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDate
import datetime
from dateutil.relativedelta import relativedelta
from confirmation_window import ConfirmationWindow
from database_manager import DBManager
from PyQt5.QtCore import pyqtSignal

class InstructionManager( QWidget ):
    signal: pyqtSignal = pyqtSignal()
    def __init__( self ) -> None:
        QWidget.__init__( self )
        loadUi( "ui/add_instruction.ui", self )
        self.setStyleSheet( open( "ui/instruction_manager.css" ).read() )
        self.setWindowFlag( Qt.FramelessWindowHint )
        self.close_button.clicked.connect( self.close )
        self.add_button.clicked.connect( self.add_instruction )
        self.frequency_combobox.addItems([str(i) for i in range(1, 13)])
        self.database: DBManager = DBManager()
        self.confirmation_window: ConfirmationWindow = ConfirmationWindow()
        self.confirmation_window.signal.connect( self.delete_instruction )
        self.select_button.clicked.connect( self.select_file )
        self.add_button.clicked.connect(self.add_instruction)
        self.validation_date.setDate( QDate.currentDate() )
        self.instruction_id: int = None


    def select_file( self ) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "../../resources/pdf", "PDF files (*.pdf)")
        file_name: str = path.split("/")[-1]
        self.path_label.setText(file_name)

    def delete_instruction( self ) -> None:
        query = f"delete from instructions where id = {self.instruction_id}"
        self.database.execute_query( query )
        self.instruction_id = None
        self.signal.emit()


    def display_window( self ):
        self.hide()
        self.show()
        
    def add_instruction( self ) -> None:
        name: str = self.instruction_name.text()
        path: str = self.path_label.text()
        validation_date: QDate = self.validation_date.date()
        frequency: int = int(self.frequency_combobox.currentText())
        if path == "" or name == "":
            return
        validation_date: str = validation_date.toString('yyyy-MM-dd')
        validation_date_converted: datetime = datetime.datetime.strptime( validation_date, '%Y-%m-%d' )
        expiration_date = validation_date_converted + relativedelta( months=+frequency )
        query = f" insert into instructions ( name, file_path, validation_date, expiration_date )\
        values('{name}','{path}','{validation_date}','{expiration_date.date()}')"
        self.database.execute_query( query )
        self.signal.emit()
        self.hide()


    def confirmation( self, instruction_id ) -> None:
        self.confirmation_window.hide()
        self.instruction_id = instruction_id
        # name = [ (name, ) ]
        name: list[ tuple ] = self.database.execute_query( f"select name from instructions where id = {instruction_id}")
        self.confirmation_window.set_title( name[ 0 ][ 0 ] )
        self.confirmation_window.show()







