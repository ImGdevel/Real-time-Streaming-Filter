import sys
import cv2
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget


class CaptureWindow(QDialog):
    photo_captured = Signal(QImage)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Capture")
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # 종료 버튼만 있는 Dialog

        self.video_frame = QLabel()
        self.capture_button = QPushButton("Capture")
        self.close_button = QPushButton("Close")

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.capture_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.capture_button.clicked.connect(self.capture_frame)
        self.close_button.clicked.connect(self.close_and_release_capture)

        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.timer.start(1000 / 30)  # 30 fps

    def closeEvent(self, event):
        self.close_and_release_capture()
        event.accept()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.video_frame.setPixmap(QPixmap.fromImage(q_img))

    def capture_frame(self):
        ret, frame = self.cap.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            q_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            self.photo_captured.emit(q_img)
            self.close_and_release_capture()

    def close_and_release_capture(self):
        self.timer.stop()
        self.cap.release()
        self.close()
