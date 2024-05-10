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
        self.current_webcam = 0

    class WindowCapture:
        def __init__(self, window_name=None, capture_rate=30, region=None, processor = None):
            self.window_name = window_name
            self.wait_time = 1/capture_rate
            self.region = region
            self.processor = processor
            self.frame=self.screenshot()
            

        def screenshot(self):
            import pyautogui
            import numpy as np
            region = self.region
            frame = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region)), cv2.COLOR_RGB2BGR)
            
            processed_frame = self.processor.process_frame(frame)

            return processed_frame

    def run(self):
        ESC_KEY=27
        FRAME_RATE = 60
        SLEEP_TIME = 1/FRAME_RATE
        capture = self.WindowCapture(region=(0, 0, 600, 500), capture_rate=FRAME_RATE, processor=self)
        

        while True:
            start=time.time()
            frame = capture.screenshot()
            cv2.imshow("frame1",frame)
            delta= time.time()-start
            if delta <SLEEP_TIME:
                time.sleep(SLEEP_TIME-delta)
            key= cv2.waitKey(1) & 0xFF
            if key== ESC_KEY:
                break

    def process_frame(self, frame):
        '''프레임 처리 메서드 - 얼굴 모자이크 및 객체 인식'''
        processed_frame = frame
        boxesList = self.filtering.video_filtering(frame)    
        for key in boxesList.keys():
            if key == -1:
                if boxesList[key] is not None:
                    processed_frame = self.filtering.blur(frame, boxesList[key])
            elif key == -2:
                if boxesList[key] is not None:
                    processed_frame = self.filtering.square_blur(frame, boxesList[key])
            else:
                if boxesList[key] is not None:
                    processed_frame = self.filtering.face_sticker(frame, boxesList[key], key)
    
        return processed_frame
    
    def set_filter(self, filter):
        """필터 설정"""
        if filter is not None:
            current_filter = self.filter_manager.get_filter(filter)
            self.filtering.set_filter(current_filter)
        else: 
            self.filtering.set_filter(None)

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
        self.is_running = False
        self.quit()
        self.video_cap.release()
        self.video_cap = None

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