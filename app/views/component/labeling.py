from utils import Colors, Style
from PySide6.QtWidgets import (
     QFrame, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QScrollArea, QCheckBox, QSlider, QSizePolicy
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize, Signal

class ContentLabeling(QWidget):

    def __init__(self,  parent = None,) -> None:
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 2, 10, 0)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        
        self.label = QLabel("")
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 5, 0, 0)
        
        self.content = QWidget()
        self.content.setStyleSheet(Style.frame_style)
        self.content.setLayout(self.content_layout)
        
        layout.addWidget(self.label)
        layout.addWidget(self.content)
        self.setLayout(layout)
        
    def setContent(self, contnet: QWidget):
        self.content_layout.addWidget(contnet)
        
    
    def setLabel(self, text, style:str = Style.title_label):
        self.label.setText(text)
        self.label.setStyleSheet(style)
        
    def setContentMargin(self, left, top, right, bottom):
        self.content_layout.setContentsMargins(left, top, right, bottom)
    
    
        