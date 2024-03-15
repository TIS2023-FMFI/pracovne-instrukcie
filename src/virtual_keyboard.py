import sys
import configparser

from PyQt5.QtCore import Qt, QEvent, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QDesktopWidget

BACKSPACE = '⌫'
SPACE = ' '
SHIFT = '⇧'
ENTER = '⏎'


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

        self.oldPos = None
        self.shift = False
        self.buttons = []

        # Create buttons for the keyboard
        self.keyboard_layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', BACKSPACE],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            [SHIFT, 'z', 'x', 'c', 'v', 'b', 'n', 'm', ENTER],
            [SPACE]
        ]

        for row in self.keyboard_layout:
            row_layout = QHBoxLayout()
            for key in row:
                button = QPushButton(key)
                button.clicked.connect(self.on_button_clicked)
                if key == ENTER:
                    button.setStyleSheet("font-size: 20px;")

                row_layout.addWidget(button)
                self.buttons.append(button)

            self.layout.addLayout(row_layout)

        width, height = get_screen_resolution()
        self.move(width // 2 - 150, height - self.height())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def set_input_line(self, input_line):
        self.input = input_line

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            self.close()
            return True

        return super().eventFilter(obj, event)

    def on_button_clicked(self):
        button = self.sender()
        if button:
            char = button.text()
            if char == SHIFT:
                if not self.shift:
                    self.enable_shift()

                else:
                    self.disable_shift()

            else:
                if self.shift:
                    self.disable_shift()

                if char == ENTER:
                    self.close()

                elif char == BACKSPACE:
                    self.input.setText(self.input.text()[:-1])

                elif char == SPACE:
                    self.input.setText(self.input.text() + ' ')

                else:
                    self.input.setText(self.input.text() + char)

    def enable_shift(self):
        self.shift = True

        for button in self.buttons:
            button.setText(button.text().upper())

    def disable_shift(self):
        self.shift = False

        for button in self.buttons:
            button.setText(button.text().lower())
