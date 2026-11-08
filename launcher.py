import os
import sys

if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))

from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())
