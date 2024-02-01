
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel, QPushButton, \
    QToolButton, QSpacerItem
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   


class ConfirmationWindow( QWidget ):
    signal = pyqtSignal()
    def __init__( self ) -> None:
        QWidget.__init__(self)
        loadUi( "ui/confirmation_window.ui", self )
        self.setWindowFlag( Qt.FramelessWindowHint )
        self.setStyleSheet( open( 'ui/confirmation_window.css' ).read() )
       
        self.reject_button.clicked.connect( self.close )
        self.accept_button.clicked.connect( self.confirm )
       

    def confirm( self ) -> None:
        self.signal.emit()
        self.close()
        
    
    def set_title( self, name ) -> None:
        text = "Vymazať " + name + "?"
        self.title.setText( text )



