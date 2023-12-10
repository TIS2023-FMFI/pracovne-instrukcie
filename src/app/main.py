import sys
import os
import fitz
import ctypes
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QListView, \
QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QGraphicsLineItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter, QPen
from PyQt5.QtCore import QModelIndex, QAbstractListModel, QSize, Qt, QUrl





class LoginWindow(QDialog):
    def __init__(self) -> None:
        super(LoginWindow, self).__init__()
        loadUi('ui/login.ui', self)
        self.main_window = MainWindow(self)

        self.login_button.clicked.connect(self.log_in)
        self.showFullScreen()

    def log_in(self) -> None:
        # TODO: login logistics
        self.main_window.showFullScreen()
        self.hide()


class MainWindow(QMainWindow):
    def __init__(self, login_window) -> None:
        self.login_window: QDialog = login_window
        super(MainWindow, self).__init__()
        loadUi('ui/main_window.ui', self)

        self.logout_button.clicked.connect(self.log_out)
        self.model: QStandardItemModel = QStandardItemModel()
        self.instructions_dir: str = "../../resources/pdf/"
        self.instructions: list[ str ] = [ self.instructions_dir + instruction for instruction in os.listdir( self.instructions_dir ) if instruction.endswith( ".pdf" ) ]
        self.pdf_viewer: PDFViewer = PDFViewer( self )
        self.display_instructions()
        


    def log_out(self) -> None:
        self.hide()
        self.login_window.showFullScreen()

    def display_instructions( self ) -> None:
        
        self.listView.setModel( self.model )
        self.listView.setMovement( QListView.Movement.Free )
        
        instruction_names: str = [ instruction for instruction in os.listdir( self.instructions_dir ) if instruction.endswith( ".pdf" ) ]
        self.listView.clicked[ QModelIndex ].connect( self.clicked )
        for instruction in instruction_names:
            element: QStandardItem = QStandardItem( instruction.removesuffix( ".pdf" ) )
            element.setEditable( False )
            element.setDragEnabled( False )
            element.setDropEnabled( False )
            self.model.appendRow( element )
        
    def clicked( self, index ) -> None:
        item: QStandardItem = self.model.itemFromIndex( index )
        self.open_instruction( item.text() )

    def open_instruction( self, file_name ) -> None:
        #get display name from file name dict
        name: str = file_name
        self.pdf_viewer.set_document( self.instructions_dir + file_name + '.pdf', name )
        self.pdf_viewer.display()
        

        
        
class PDFViewer( QMainWindow ):
    def __init__(self, parent, pdf_path = None, name = None ) -> None:
        super().__init__( parent )
        self.screen_width, self.screen_height = self.get_screen_resolution()
        self.w: int = 1000
        self.h: int = self.screen_height - 100
        self.path: str = pdf_path
        self.name: str = name
        self.pdf_document = fitz.open( self.path )
        self.setGeometry( ( self.screen_width - self.w ) // 2, 50, self.w , self.h )
        
    def set_document( self, path: str, name: str ) -> None:
        self.path = path
        self.name = name
        self.pdf_document = fitz.open( self.path )
        self.setWindowTitle( self.name )

    def get_screen_resolution( self ) -> tuple[ int ]:
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics( 0 )
        screen_height = user32.GetSystemMetrics( 1 )
        return screen_width, screen_height

    def resize_page( self, page: fitz.Page ) -> fitz.Pixmap:
        w, h = page.rect.br
        zoom = self.w / w * 0.96
        matrix = fitz.Matrix( zoom, zoom )
        return page.get_pixmap( matrix = matrix )

    def display( self ) -> None:
        # Create QGraphicsView for displaying PDF pages
        graphics_view = QGraphicsView( self )
        graphics_view.setAlignment( Qt.AlignTop | Qt.AlignCenter )
        # Create QGraphicsScene with a vertical layout
        scene = QGraphicsScene( self )
        graphics_view.setScene( scene )
        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(graphics_view)
        # Display all pages with lines between them
        y_position = 0
        for page_number in range( self.pdf_document.page_count ):
            pixmap = QPixmap()
            pdf_page = self.pdf_document[ page_number ]
            image = self.resize_page( pdf_page )

            pixmap.loadFromData( image.tobytes() )
            pixmap_item = QGraphicsPixmapItem( pixmap )
            scene.addItem( pixmap_item )
            pixmap_item.setPos( 0, y_position )
            y_position += pixmap_item.pixmap().height()
            # Draw a line between pages
            if page_number < self.pdf_document.page_count - 1:
                line = QGraphicsLineItem( 0, y_position, pixmap.width(), y_position )
                scene.addItem( line )
                y_position += 1  # height of line

        # Create central widget
        container = QDialog()
        container.setLayout( layout )
        self.setCentralWidget( container )
        self.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = LoginWindow()
    app.exec()
