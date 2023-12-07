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

    def open_instruction( self, name ) -> None:
        self.pdf_viewer.set_path( self.instructions_dir + name + '.pdf' )
        self.pdf_viewer.display()
        

        
        
class PDFViewer( QMainWindow ):
    def __init__(self, parent, pdf_path = None ) -> None:
        super().__init__( parent )

        self.setWindowTitle('PDF Viewer')
        self.w, self.h = self.get_screen_resolution()
        self.setGeometry( self.w // 2 - 500 , 100, 1000 , self.h - 200 )
        self.path: str = pdf_path
    
    def set_path( self, path ) -> None:
        self.path = path
    
    def get_screen_resolution( self ) -> tuple[ int ]:
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height

    def display( self ) -> None:
        # Load the PDF document
        self.pdf_document = fitz.open( self.path )
        self.current_page = 0

        # Create QGraphicsView for displaying PDF pages
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Create QGraphicsScene with a vertical layout
        self.scene = QGraphicsScene(self)
        
        self.graphics_view.setScene(self.scene)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.graphics_view)

        # Display all pages with lines between them
        y_position = 0
        for page_number in range(self.pdf_document.page_count):
            pdf_page = self.pdf_document[ page_number ]
            
            image = pdf_page.get_pixmap()
            pixmap = QPixmap()
            pixmap.loadFromData(image.tobytes())
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(pixmap_item)
            pixmap_item.setPos(0, y_position)
            y_position += pixmap_item.pixmap().height()
            # Draw a line between pages
            if page_number < self.pdf_document.page_count - 1:
                line = QGraphicsLineItem(0, y_position, pixmap.width(), y_position)
                self.scene.addItem(line)

                y_position += 1  # height of line

        # Create central widget
        container = QDialog()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('ui/login.css').read())
    w = LoginWindow()
    app.exec()
