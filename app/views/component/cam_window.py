from PySide6.QtCore import  Qt
from PySide6.QtGui import QImage, QPixmap, QColor
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
                            
        self.show_box = QLabel(self)
        self.show_box.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.show_box.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        layout.addWidget(self.show_box)
        
        self.setMinimumSize(1, 1)  # 최소 크기 지정

    def update_frame(self, frame: QImage = None):
        """프레임 업데이트"""
        if frame is None or frame.isNull():
            self.frame_clear()
            return 

        if not self.is_setInitWindowSize:
            self.resize(frame.width(), frame.height())
            self.is_setInitWindowSize = True
            pixmap = QPixmap.fromImage(frame)
            self.show_box.setPixmap(pixmap)

        pixmap = QPixmap.fromImage(frame)
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio)

        self.show_box.setPixmap(pixmap)

    def frame_clear(self):
        empty_frame = QImage(10, 10, QImage.Format_RGB888)
        empty_frame.fill(QColor(23, 26, 30))
        pixmap = QPixmap.fromImage(empty_frame)
        scaled_image = pixmap.scaled(self.show_box.width(), self.show_box.height(), Qt.KeepAspectRatio,  Qt.SmoothTransformation)
        self.show_box.setPixmap(scaled_image)


    def resizeEvent(self, event):
        """윈도우 크기 조절 이벤트"""
        super().resizeEvent(event)
        if not self.show_box.pixmap():
            return
        pixmap = self.show_box.pixmap().scaled(self.size(), Qt.KeepAspectRatio)

        self.show_box.setPixmap(pixmap)

    def showEvent(self, event):
        # Dialog가 보일 때 실행되는 코드
        self.is_setInitWindowSize = False