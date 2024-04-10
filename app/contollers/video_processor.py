from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal
import cv2

# 비디오 처리 스레드
class VideoProcessor(QThread):
    frame_ready = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.video_cap = cv2.VideoCapture(0)  # 웹캠 캡처 객체
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # 얼굴 인식을 위한 분류기
        self.is_running = False  # 스레드 실행 상태
        self.is_flipped = False  # 화면 좌우 뒤집기 상태
        self.mosaic_active = False  # 모자이크 활성화 상태

    def run(self):
        '''스레드 실행 메서드 - 웹캠에서 프레임을 읽어와 RGB 형식으로 변환.'''
        self.is_running = True
        while self.is_running:
            ret, frame = self.video_cap.read()  # 웹캠에서 프레임 읽기
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
                if self.is_flipped:
                    frame_rgb = cv2.flip(frame_rgb, 1)  # 화면 좌우 뒤집기
                
                if self.mosaic_active:
                    frame_rgb = self.apply_mosaic(frame_rgb)

                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(q_img)  # 프레임을 GUI로 전송
            self.msleep(16)  # 약 60fps

    def stop(self):
        '''스레드 종료 메서드'''
        self.is_running = False
        self.wait()

    def flip_horizontal(self):
        '''화면 좌우 뒤집기 메서드'''
        self.is_flipped = not self.is_flipped  # 화면 좌우 뒤집기 상태 변경

    def apply_mosaic(self, frame_rgb):
        '''모자이크 처리 메서드'''
        faces = self.face_cascade.detectMultiScale(frame_rgb, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
        for (x, y, w, h) in faces:
            face_img = frame_rgb[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (w//10, h//10))
            face_img = cv2.resize(face_img, (w, h), interpolation=cv2.INTER_AREA)
            frame_rgb[y:y+h, x:x+w] = face_img
        
        return frame_rgb