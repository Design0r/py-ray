import sys
from PySide6.QtWidgets import *
from pyray.window import Window


app = QApplication(sys.argv)
update_screen = Window((1000, 700))

sys.exit(app.exec())
