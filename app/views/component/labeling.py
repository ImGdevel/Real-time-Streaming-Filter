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
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        frame = QWidget()
        
        content_label_layout = QVBoxLayout()
        content_label_layout.setContentsMargins(10, 2, 10, 0)
        content_label_layout.setSpacing(5)
        content_label_layout.setAlignment(Qt.AlignTop)
        
        self.label = QLabel("")
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 5, 0, 5)
        
        self.content = QWidget()
        self.content.setStyleSheet(Style.frame_style)
        self.content.setLayout(self.content_layout)
        
        content_label_layout.addWidget(self.label)
        content_label_layout.addWidget(self.content)
        
        frame.setLayout(content_label_layout)
        layout.addWidget(frame)
        
        self.setLayout(layout)
        
    def setContent(self, contnet: QWidget):
        self.content_layout.addWidget(contnet)
        
    
    def setLabel(self, text, style:str = Style.title_label):
        self.label.setText(text)
        self.label.setStyleSheet(style)
        
    def setContentMargin(self, left, top, right, bottom):
        self.content_layout.setContentsMargins(left, top, right, bottom)
    
    
        