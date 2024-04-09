from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from ui.video_processor import VideoProcessor
from ui.colors import Colors

class StreamWidget(QWidget):
    def __init__(self):
        self.super().__init__()
        self.setStream()
    
    def setStream(self):
        self.video_label = QLabel()
        self.video_processor = VideoProcessor()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frame = self.video_processor.get_frame()

        if frame is not None:
            # 원본 영상
            q_img1 = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap1 = QPixmap.fromImage(q_img1).scaled(320, 240, aspectRatioMode=Qt.KeepAspectRatio)
            self.video_label.setPixmap(pixmap1)
            



