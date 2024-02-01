import sys
import os

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel, QPushButton, \
    QToolButton, QSpacerItem

from confirmation_window import ConfirmationWindow
from database_manager import DBManager
class InstructionManager( QWidget ):
    def __init__( self ) -> None:
        QWidget.__init__( self )
        loadUi( "ui/add_instruction.ui", self )
        self.setStyleSheet( open( "ui/instruction_manager.css" ).read() )
        self.setWindowFlag( Qt.FramelessWindowHint )
        self.close_button.clicked.connect( self.close )
        self.add_button.clicked.connect( self.add_instruction )
        self.frequency_combobox.addItems([str(i) for i in range(1, 13)])
        self.database = DBManager()
        self.confirmation_window = ConfirmationWindow()
        self.confirmation_window.signal.connect( self.delete_instruction )
        self.instruction_id = None





    def delete_instruction( self ):
        query = f"delete from instructions where id = {self.instruction_id}"
        self.database.execute_query( query )
        self.instruction_id = None

    def add_instruction( self ):
        ...


    def confirmation( self, instruction_id ):
        self.confirmation_window.hide()
        # name = [ (name, ) ]
        self.instruction_id = instruction_id
        name = self.database.execute_query( f"select name from instructions where id = {instruction_id}")
        self.confirmation_window.set_title( name[ 0 ][ 0 ] )
        self.confirmation_window.show()







