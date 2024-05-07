import cv2
from PySide6.QtGui import QImage
from PySide6.QtCore import QThread, Signal
from models import Filtering, FilterManager
import time

# 비디오 처리 스레드
class RealStreamProcessor(QThread):
    frame_ready = Signal(QImage)

    def __init__(self):
        super().__init__()
        self.video_cap = cv2.VideoCapture(0)  # 웹캠 캡처 객체
        self.filtering = Filtering()
        self.filter_manager = FilterManager()

        self.is_running = False  # 스레드 실행 상태
        self.is_flipped = True  # 화면 좌우 뒤집기 상태
        self.current_webcam = None

    def run(self):
        '''스레드 실행 메서드 - 웹캠에서 프레임을 읽어와 RGB 형식으로 변환.'''
        self.is_running = True
        while self.is_running:
            #start = time.time()
            ret, frame = self.video_cap.read()  # 웹캠에서 프레임 읽기
            if ret:
                processed_frame = self.process_frame(frame)  # 프레임 처리
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환

                if self.is_flipped:
                    frame_rgb = cv2.flip(frame_rgb, 1)  # 화면 좌우 뒤집기

                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(q_img)  # 프레임을 GUI로 전송
            #end = time.time()
            #result = end - start
            # print("time: "+ str(result))

    def process_frame(self, frame):
        '''프레임 처리 메서드 - 얼굴 모자이크 및 객체 인식'''
        processed_frame = frame
        boxesList = self.filtering.video_filtering(frame)    
        for key in boxesList.keys():
            if key == -1:
                processed_frame = self.filtering.blur(frame, boxesList[key])
            elif key == -2:
                processed_frame = self.filtering.square_blur(frame, boxesList[key])
            else:
                processed_frame = self.filtering.face_sticker(frame, boxesList[key], key)
    
        return processed_frame
    
    def set_filter(self, filter):
        """필터 설정"""
        if not filter is None:
            current_filter = self.filter_manager.get_filter(filter)
            self.filtering.set_filter(current_filter)

    def flip_horizontal(self):
        '''화면 좌우 뒤집기 메서드'''
        self.is_flipped = not self.is_flipped  # 화면 좌우 뒤집기 상태 변경


    def pause(self):
        '''스레드 일시 중지'''
        self.is_running = False
        self.filtering.tracking_id_init()
        self.wait()

    def stop(self):
        '''스레드 종료 메서드'''
        self.quit()

    def set_web_cam(self, web_cam):
        '''웹캠 설정'''
        if self.isRunning():
            self.pause()  # 스레드가 실행 중이면 중지
        
        if self.current_webcam != web_cam:  # 새로운 웹캠이 이전과 다를 경우에만 설정 변경
            if self.video_cap is not None:
                self.video_cap.release()  # 이전 웹캠 해제
            self.video_cap = cv2.VideoCapture(web_cam)  # 새로운 웹캠 연결
            self.current_webcam = web_cam  # 현재 연결된 웹캠 번호 업데이트

        if self.isRunning():
            self.start()  # 스레드를 다시 시작