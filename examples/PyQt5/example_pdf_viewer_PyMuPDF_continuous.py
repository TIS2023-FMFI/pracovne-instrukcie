import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, \
    QWidget, QGraphicsLineItem
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt


class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()

        self.setWindowTitle('PDF Viewer')
        self.setGeometry(100, 100, 631, 910)

        # Load the PDF document
        self.pdf_document = fitz.open(pdf_path)
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
            pdf_page = self.pdf_document[page_number]
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
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    viewer = PDFViewer(pdf_path='../../docs/Katalog_Poziadaviek.pdf')
    viewer.show()

    sys.exit(app.exec_())
