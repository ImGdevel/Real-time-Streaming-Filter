import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2

class VideoProcessor:
    def __init__(self):
        self.video_cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def get_frame(self):
        ret, frame = self.video_cap.read()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None

    def mosaic_face(self, frame):
        mosaic_frame = frame.copy()
        gray = cv2.cvtColor(mosaic_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            roi = mosaic_frame[y:y+h, x:x+w]
            roi = cv2.resize(roi, (w//15, h//15), interpolation=cv2.INTER_LINEAR)
            roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
            mosaic_frame[y:y+h, x:x+w] = roi
        
        return mosaic_frame

    def convert_to_grayscale(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB)
    
    def invert_colors(self, frame):
        frame_inverted = cv2.bitwise_not(frame)
        return cv2.cvtColor(frame_inverted, cv2.COLOR_BGR2RGB)

class VideoStream(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Stream")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 수평 박스 레이아웃 생성
        self.layout = QHBoxLayout()

        # 수직 박스 레이아웃 생성 (버튼을 수직으로 배치하기 위해)
        self.button_layout = QVBoxLayout()

        self.gray_button = QPushButton("Grayscale Mode (OFF)")
        self.gray_button.setCheckable(True)
        self.gray_button.clicked.connect(self.toggle_gray_mode)
        self.button_layout.addWidget(self.gray_button)

        self.invert_button = QPushButton("Invert Mode (OFF)")
        self.invert_button.setCheckable(True)
        self.invert_button.clicked.connect(self.toggle_invert_mode)
        self.button_layout.addWidget(self.invert_button)

        self.mosaic_button = QPushButton("Mosaic Mode (OFF)")
        self.mosaic_button.setCheckable(True)
        self.mosaic_button.clicked.connect(self.toggle_mosaic_mode)
        self.button_layout.addWidget(self.mosaic_button)

        # 빈 QLabel을 추가하여 버튼들이 아래쪽으로 정렬되도록 함
        self.button_layout.addWidget(QLabel())

        self.layout.addLayout(self.button_layout)

        # 수직 박스 레이아웃 생성 (영상을 수직으로 배치하기 위해)
        self.video_layout = QVBoxLayout()

        self.video_label1 = QLabel()
        self.video_label2 = QLabel()

        self.video_layout.addWidget(self.video_label1)
        self.video_layout.addWidget(self.video_label2)

        self.layout.addLayout(self.video_layout)

        self.central_widget.setLayout(self.layout)

        self.video_processor = VideoProcessor()  # VideoProcessor 객체 생성

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.gray_mode = False
        self.invert_mode = False
        self.mosaic_mode = False

    def toggle_gray_mode(self, checked):
        self.gray_mode = checked
        if self.gray_mode:
            self.gray_button.setText("Grayscale Mode (ON)")
        else:
            self.gray_button.setText("Grayscale Mode (OFF)")
        self.update_frame()

    def toggle_invert_mode(self, checked):
        self.invert_mode = checked
        if self.invert_mode:
            self.invert_button.setText("Invert Mode (ON)")
        else:
            self.invert_button.setText("Invert Mode (OFF)")
        self.update_frame()

    def toggle_mosaic_mode(self, checked):
        self.mosaic_mode = checked
        if self.mosaic_mode:
            self.mosaic_button.setText("Mosaic Mode (ON)")
        else:
            self.mosaic_button.setText("Mosaic Mode (OFF)")
        self.update_frame()

    def update_frame(self):
        frame = self.video_processor.get_frame()

        if frame is not None:
            # 원본 영상
            q_img1 = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap1 = QPixmap.fromImage(q_img1).scaled(320, 240, aspectRatioMode=Qt.KeepAspectRatio)
            self.video_label1.setPixmap(pixmap1)

            # 영상 처리
            if self.gray_mode:
                processed_frame = self.video_processor.convert_to_grayscale(frame)
            elif self.invert_mode:
                processed_frame = self.video_processor.invert_colors(frame)
            elif self.mosaic_mode:
                processed_frame = self.video_processor.mosaic_face(frame.copy())  # 원본 프레임의 복사본을 사용
            else:
                processed_frame = frame
            
            q_img2 = QImage(processed_frame.data, processed_frame.shape[1], processed_frame.shape[0], QImage.Format_RGB888)
            pixmap2 = QPixmap.fromImage(q_img2).scaled(320, 240, aspectRatioMode=Qt.KeepAspectRatio)
            self.video_label2.setPixmap(pixmap2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoStream()
    window.show()
    sys.exit(app.exec_())
