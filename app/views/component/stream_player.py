from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from utils import Colors
from .focus_detect_select_area import FocusDetectSelectArea

class StreamVideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.focusSelectMode = True
        self.initUI()

    def initUI(self):
        video_layout = QHBoxLayout()

        self.show_box = QLabel()
        self.show_box.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.show_box.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        video_layout.addWidget(self.show_box)
        self.show_box.setMaximumWidth(725)

        # FocusDetectSelectArea를 show_box와 동일한 위치와 크기로 추가
        self.overlay = FocusDetectSelectArea(self.show_box)
        self.overlay.setGeometry(0, 0, self.show_box.width(), self.show_box.height())
        self.overlay.raise_()

        self.setLayout(video_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # show_box가 리사이즈 될 때 overlay도 리사이즈
        self.overlay.setGeometry(0, 0, self.show_box.width(), self.show_box.height())

    def update_video(self, frame: QImage = None):
        '''비디오 업데이트 메서드'''
        if frame is None:
            return
        pixmap = QPixmap.fromImage(frame)
        self.show_box.setPixmap(pixmap.scaled(self.show_box.width(), self.show_box.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def enterEvent(self, event):
        if self.focusSelectMode:
            self.show_box.setCursor(Qt.CrossCursor)

    def setMode(self, mode : bool):
        self.focusSelectMode = mode
    
    def setSize(self, size:QSize):
        self.video_size = size
