from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from database_manager import DBManager




class Validation( QWidget ):
    def __init__( self ) -> None:
        QWidget.__init__( self )
        loadUi( "ui/validation.ui", self )
        self.setStyleSheet( open( 'ui/validation.css' ).read() )
        self.setWindowFlag( Qt.FramelessWindowHint )
        self.close_button.clicked.connect( lambda: self.hide() )
        self.select_button.clicked.connect( self.select_file )
        self.validate_button.clicked.connect( self.validate )
        self.frequency_option.addItems( map( str, range( 1, 13 ) ) )
        self.database = DBManager()
        self.file_path = None
        self.file_name = None





    def select_file( self ) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName( self, "Select file", "../../resources/pdf","PDF files (*.pdf)" )
        file_name = path.split( "/" )[ -1 ]
        self.path_label.setText( file_name )

    def set_file( self, name, path ):
        self.file_path = path
        self.file_name = name
        self.lineEdit.setText( name )

    def validate( self ):
        self.database.execute_query( f"Insert into validations (name) values('{self.file_name}')" )
        print(self.database.execute_query( f"select * from validations") )
        self.file_path = None
        self.file_name = None
        self.hide()