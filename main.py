import sys
from PySide6.QtWidgets import QApplication
from pyray.window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_screen = Window((1000, 700))

    sys.exit(app.exec())
