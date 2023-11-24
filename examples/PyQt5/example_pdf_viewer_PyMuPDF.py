import sys
import fitz  # PyMuPDF

from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, \
    QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()

        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 620, 910)

        # Load the PDF document
        self.pdf_document = fitz.open(pdf_path)
        self.current_page = 0

        # Create QGraphicsView for displaying PDF pages
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setCentralWidget(self.graphics_view)

        # Create QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        # Navigation buttons
        self.prev_button = QPushButton('Previous Page', self)
        self.next_button = QPushButton('Next Page', self)

        # Connect buttons to the display_page method
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        # Layout setup
        layout = QVBoxLayout()  # Outer vertical layout

        # Add the QGraphicsView to the outer vertical layout
        layout.addWidget(self.graphics_view)

        # Nested horizontal layout for the buttons
        buttons_layout = QHBoxLayout()

        # Add the buttons to the nested layout
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.next_button)

        # Add the nested layout to the outer vertical layout
        layout.addLayout(buttons_layout)

        # Create central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Display the first page
        self.display_page(self.current_page)

    def display_page(self, page_number):
        if 0 <= page_number < self.pdf_document.page_count:
            self.current_page = page_number

            # Get the PDF page
            pdf_page = self.pdf_document[page_number]

            # Render the PDF page to a pixmap
            image = pdf_page.get_pixmap()
            pixmap = QPixmap()
            pixmap.loadFromData(image.tobytes())

            # Display the pixmap in QGraphicsPixmapItem
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()
            self.scene.addItem(pixmap_item)

            # Set the scene size
            self.scene.setSceneRect(0, 0, pixmap_item.pixmap().width(), pixmap_item.pixmap().height())

    def prev_page(self):
        self.display_page(self.current_page - 1)

    def next_page(self):
        self.display_page(self.current_page + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    viewer = PDFViewer(pdf_path='../../docs/Katalog_Poziadaviek.pdf')
    viewer.show()

    sys.exit(app.exec_())
