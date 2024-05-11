from PySide6.QtCore import  Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from utils import Colors

class CamWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.is_setInitWindowSize = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                            
        self.video_label = QLabel(self)
        self.video_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.video_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        layout.addWidget(self.video_label)
        
        self.setMinimumSize(1, 1)  # 최소 크기 지정

    def update_frame(self, frame: QImage):
        """프레임 업데이트"""
        if not self.is_setInitWindowSize:
            self.resize(frame.width(), frame.height())
            self.is_setInitWindowSize = True
            pixmap = QPixmap.fromImage(frame)
            self.video_label.setPixmap(pixmap)

        pixmap = QPixmap.fromImage(frame)
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio)

        self.video_label.setPixmap(pixmap)


    def resizeEvent(self, event):
        """윈도우 크기 조절 이벤트"""
        super().resizeEvent(event)
        if not self.video_label.pixmap():
            return
        pixmap = self.video_label.pixmap().scaled(self.size(), Qt.KeepAspectRatio)

        self.video_label.setPixmap(pixmap)

    def showEvent(self, event):
        # Dialog가 보일 때 실행되는 코드
        self.is_setInitWindowSize = False