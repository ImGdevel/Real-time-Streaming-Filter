import cv2
import numpy as np
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from utils import Colors

class CamWindow(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.initUI()
        
    def initUI(self):
        layer = QVBoxLayout()
        layer.setContentsMargins(0,0,0,0)
        layer.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        self.dialog_videolable = QLabel()
        #self.dialog_videolable.setMinimumSize(400,300)
        #self.dialog_videolable.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 정렬 설정
        layer.addWidget(self.dialog_videolable)
        
        self.setLayout(layer)

    def update_frame(self, frame):
        """프레임 전송"""
        pixmap = QPixmap.fromImage(frame)
        self.dialog_videolable.setPixmap(pixmap)