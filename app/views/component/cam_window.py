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
        self.is_setInitWindowSize = False
        self.initUI()
        
    def initUI(self):
        layer = QVBoxLayout()
        layer.setContentsMargins(0,0,0,0)
        layer.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.dialog_videolable = QLabel()
        layer.addWidget(self.dialog_videolable)
        
        self.setLayout(layer)

    def update_frame(self, frame: QImage):
        """프레임 전송"""
        if not self.is_setInitWindowSize:
            self.resize(frame.width(), frame.height())
            self.is_setInitWindowSize = True
            
        pixmap = QPixmap.fromImage(frame)
        pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.dialog_videolable.setPixmap(pixmap)
        
    def showEvent(self, event):
        # Dialog가 보일 때 실행되는 코드
        self.is_setInitWindowSize = False

    def closeEvent(self, event):
        pass