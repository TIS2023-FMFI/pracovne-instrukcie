import fitz
import configparser

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


def get_screen_resolution() -> tuple[int, int]:
    config: configparser = configparser.ConfigParser()
    config.read('config.ini')
    return (int(config.get('Preferences', 'WIDTH')),
            int(config.get('Preferences', 'HEIGHT')))


class InstructionViewer(QWidget):
    def __init__(self, pdf_path=None, name=None) -> None:
        QWidget.__init__(self)
        loadUi('ui/pdf.ui', self)
        self.setStyleSheet(open('ui/pdf.css').read())
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.pushButton.clicked.connect(lambda: self.hide())
        self.screen_width, self.screen_height = get_screen_resolution()
        self.w: int = 1100
        self.h: int = self.screen_height - 70
        self.path: str = pdf_path
        self.name: str = name
        self.pdf_document = fitz.open(self.path)
        self.setGeometry((self.screen_width - self.w) // 2, 35, self.w, self.h)

    def set_document(self, path: str, name: str) -> None:
        self.path = path
        self.name = name
        self.pdf_document = fitz.open(self.path)
        self.label.setText(self.name)

    def resize_page(self, page: fitz.Page) -> fitz.Pixmap:
        w, h = page.rect.br
        zoom = self.w / w * 0.98
        matrix = fitz.Matrix(zoom, zoom)
        return page.get_pixmap(matrix=matrix)

    def display(self) -> None:
        # Create QGraphicsView for displaying PDF pages
        self.hide()
        self.graphicsView.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        # Create QGraphicsScene with a vertical layout
        scene = QGraphicsScene(self)
        self.graphicsView.setScene(scene)
        # Display all pages with lines between them
        y_position = 0

        for page_number in range(self.pdf_document.page_count):
            pixmap = QPixmap()
            pdf_page = self.pdf_document[page_number]
            image = self.resize_page(pdf_page)
            pixmap.loadFromData(image.tobytes())
            pixmap_item = QGraphicsPixmapItem(pixmap)
            scene.addItem(pixmap_item)
            pixmap_item.setPos(0, y_position)
            y_position += pixmap_item.pixmap().height()
            # Draw a line between pages
            if page_number < self.pdf_document.page_count - 1:
                line = QGraphicsLineItem(0, y_position, pixmap.width(), y_position)
                scene.addItem(line)
                y_position += 1  # height of line

        # Create central widget      
        self.show()
