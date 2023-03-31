from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *


class Window(QWidget):
    def __init__(self, parent=None, zoom=1) -> None:
        super().__init__(parent)
        self.width = 0
        self.height = 0
        self.move(250, 250)
        self.img = None
        self.zoom = zoom

        self.label = QLabel()
        self.my_layout = QHBoxLayout()
        self.my_layout.setContentsMargins(0, 0, 0, 0)
        self.my_layout.addWidget(self.label)
        self.setLayout(self.my_layout)

        self.setUpdatesEnabled(True)
        self.label.setUpdatesEnabled(True)

        self.setWindowTitle("PyRay")
        self.show()

    def set_width(self, width):
        self.width = width
        self.resize(self.width, self.height)
        self.label.setMinimumWidth(self.width)
        self.img = QImage(self.width/self.zoom, self.height/self.zoom, QImage.Format.Format_ARGB32)

    def set_height(self, height):
        self.height = height
        self.resize(self.width, self.height)
        self.label.setMinimumHeight(self.height)
        self.img = QImage(self.width/self.zoom, self.height/self.zoom, QImage.Format.Format_ARGB32)

    def set_pixel(self, x, y, color):
        self.img.setPixel(x, y, QColor(color.r, color.g, color.b, 1).rgb())

    def update_screen(self, sample):
        painter = QPainter(self.img)
        painter.setPen(QPen(QColor(255, 0, 0, 255)))
        painter.drawText(10, 10, str(sample))
        self.label.setPixmap(QPixmap.fromImage(self.img.scaled(self.width, self.height)))
        self.label.update()
        self.update()
