import sys
import configparser

from PyQt5.QtCore import Qt, QEvent, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QDesktopWidget

BACKSPACE = '<-'
SPACE = '-'


def get_screen_resolution() -> tuple[int, int]:
    config: configparser = configparser.ConfigParser()
    config.read('config.ini')
    return (int(config.get('Preferences', 'WIDTH')),
            int(config.get('Preferences', 'HEIGHT')))


class VirtualKeyboard(QWidget):
    def __init__(self, input_line):
        QWidget.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.installEventFilter(self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input = input_line

        # Create buttons for the keyboard
        self.keyboard_layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', BACKSPACE],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            [SPACE]
        ]

        for row in self.keyboard_layout:
            row_layout = QHBoxLayout()
            for key in row:
                button = QPushButton(key)
                button.clicked.connect(self.on_button_clicked)
                row_layout.addWidget(button)

            self.layout.addLayout(row_layout)

        width, height = get_screen_resolution()
        self.move(width // 2 - 150, height - self.height())

    def set_input_line(self, input_line):
        self.input = input_line

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusOut:
            self.hide()
            return True

        return super().eventFilter(obj, event)

    def on_button_clicked(self):
        button = self.sender()
        if button:
            char = button.text()
            if char == BACKSPACE:
                self.input.setText(self.input.text()[:-1])

            elif char == SPACE:
                self.input.setText(self.input.text() + ' ')

            else:
                self.input.setText(self.input.text() + char)
