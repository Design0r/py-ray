import sys
from PySide6.QtWidgets import *
from pyray.window import Window


app = QApplication(sys.argv)
window = Window((1000, 700), (1024, 1024))

sys.exit(app.exec())
