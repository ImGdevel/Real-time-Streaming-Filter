from utils import Colors
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt, QPoint

class FrameWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        
    