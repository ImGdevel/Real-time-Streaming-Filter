from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
from utils import Colors
import cv2

class VideoProcessor(QThread):
    frame_ready = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.video_cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.is_running = False
        self.is_flipped = False

    def run(self):
        self.is_running = True
        while self.is_running:
            ret, frame = self.video_cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.is_flipped:
                    frame_rgb = cv2.flip(frame_rgb, 1)
                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(q_img)
            self.msleep(16)  # 약 60fps


    def stop(self):
        self.is_running = False
        self.wait()

    def flip_horizontal(self):
        self.is_flipped = not self.is_flipped

class RealStreamView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 왼쪽 상단 toolbar
        self.toolbar = QWidget()
        self.toolbar.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.toolbar.setFixedSize(300, 450)
        self.layout.addWidget(self.toolbar, 0, 0)

        # 비디오 레이어
        self.video_widget = QLabel()
        self.video_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.video_widget.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_widget, 0, 1)

        # 하단 레이어
        self.bottom_widget = QWidget()
        self.bottom_layout = QVBoxLayout()
        self.bottom_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.bottom_widget.setLayout(self.bottom_layout)

        # 웹캠 시작 버튼
        self.start_button = QPushButton("Start Webcam")
        self.start_button.clicked.connect(self.start_webcam)
        self.bottom_layout.addWidget(self.start_button)

        # 이미지 좌우 반전 버튼
        self.flip_button = QPushButton("Flip Horizontal")
        self.flip_button.clicked.connect(self.flip_horizontal)
        self.bottom_layout.addWidget(self.flip_button)

        self.layout.addWidget(self.bottom_widget, 1, 0, 1, 2)

        self.setLayout(self.layout)

        # 비디오 처리를 위한 객체 초기화
        self.video_processor = VideoProcessor()
        self.video_processor.frame_ready.connect(self.update_video)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)

    def start_webcam(self):
        if not self.video_processor.isRunning():
            self.video_processor.start()
            self.start_button.setText("Stop Webcam")
            self.timer.start(0)  # 비동기적으로 프레임 업데이트

    def flip_horizontal(self):
        self.video_processor.flip_horizontal()

    def update_video(self, q_img=None):
        if q_img is None:
            return
        pixmap = QPixmap.fromImage(q_img)
        self.video_widget.setPixmap(pixmap.scaled(self.video_widget.width(), self.video_widget.height(), Qt.KeepAspectRatio))
        
    def closeEvent(self, event):
        self.video_processor.stop()
        self.timer.stop()
