from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal
import cv2

# 비디오 처리 스레드
class VideoProcessor(QThread):

    def __init__(self, video_path, video_widget):
        super().__init__()
        self.video_path = video_path
        self.video_widget = video_widget
        
