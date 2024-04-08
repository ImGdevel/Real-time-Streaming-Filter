import os
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class VideoInfo:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video_name = os.path.basename(video_path)
        self.video_extension = os.path.splitext(video_path)[1][1:].lower()
        self.video_size = os.path.getsize(video_path)

class VideoPlayerThread(QThread):
    video_frame = pyqtSignal(object)
    current_frame = pyqtSignal(int)

    def __init__(self, video_path):
        super(VideoPlayerThread, self).__init__()
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.video_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                current_frame_num = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.video_frame.emit(frame)
                self.current_frame.emit(current_frame_num)
            else:
                break
        self.cap.release()

class VideoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # 비디오 위젯 추가
        self.video_widget = QLabel(self)
        self.video_widget.setFixedSize(640, 480)
        self.layout.addWidget(self.video_widget)

        # 파일 탐색기 버튼
        self.file_dialog_button = QPushButton("Choose Video File")
        self.file_dialog_button.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.file_dialog_button)

        # 비디오 바 (슬라이더)
        self.video_bar = QSlider(Qt.Horizontal)
        self.video_bar.setEnabled(False)
        self.video_bar.sliderMoved.connect(self.changeVideoPosition)
        self.layout.addWidget(self.video_bar)

        self.setLayout(self.layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.video_info = VideoInfo(filePath)
            self.video_thread = VideoPlayerThread(filePath)
            self.video_thread.video_frame.connect(self.updateVideoFrame)
            self.video_thread.current_frame.connect(self.updateVideoBar)
            self.video_bar.setEnabled(True)
            self.video_thread.start()

    def updateVideoFrame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_frame.shape
        q_img = QImage(rgb_frame.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_widget.setPixmap(pixmap.scaled(self.video_widget.width(), self.video_widget.height()))

    def updateVideoBar(self, current_frame_num):
        total_frames = self.video_thread.video_frame_count
        value = int((current_frame_num / total_frames) * 100)
        self.video_bar.setValue(value)

    def changeVideoPosition(self, value):
        if hasattr(self, 'video_thread'):
            total_frames = self.video_thread.video_frame_count
            target_frame = int(value / 100 * total_frames)
            self.video_thread.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
