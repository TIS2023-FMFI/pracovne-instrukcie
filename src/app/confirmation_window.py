from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal   


class ConfirmationWindow( QWidget ):
    signal: pyqtSignal = pyqtSignal()
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
        text: str = "Vymazať " + name + " ?"
        self.title.setText( text )



