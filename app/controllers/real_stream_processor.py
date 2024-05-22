from datetime import datetime
import cv2
from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import QThread, Signal
from models import Filtering, FilterManager, PathManager
from models import DragArea
import time, os
import pyvirtualcam

# 비디오 처리 스레드
class RealStreamProcessor(QThread):
    webcam_start = Signal()
    frame_ready = Signal(QImage)
    screen_size = Signal(tuple)
    
    def __init__(self):
        super().__init__()
        self.video_cap = None  # 웹캠 캡처 객체
        self.filtering = Filtering()
        self.filter_manager = FilterManager()
        self.path_manager = PathManager()
        self.capture = None

        self.is_running = False  # 스레드 실행 상태
        self.webcam_on = False
        self.current_webcam = 0
        self.capture_mode = 0
        self.capture_area = None
        self.video_path: str = None
        self.is_record = False
        self.output_video = None
        self.focus_detection_area = None

        self.virtual_cam_backend = self.detect_virtual_cam_backend()  # 가상 카메라 백엔드 탐지

    def detect_virtual_cam_backend(self):
        '''설치된 가상 카메라 백엔드를 탐지합니다.'''
        try:
            with pyvirtualcam.Camera(width=640, height=480, fps=30, backend='obs', fmt=pyvirtualcam.PixelFormat.BGR) as cam:
                return 'obs'
        except RuntimeError:
            pass
        try:
            with pyvirtualcam.Camera(width=640, height=480, fps=30, backend='unitycapture', fmt=pyvirtualcam.PixelFormat.BGR) as cam:
                return 'unitycapture'
        except RuntimeError:
            pass
        return None

    class WindowCapture:
        def __init__(self, window_name=None, capture_rate=30, region=None, processor=None):
            self.window_name = window_name
            self.wait_time = 1 / capture_rate
            self.region = region
            self.processor = processor
            self.frame = self.screenshot()
            
        def screenshot(self):
            import pyautogui
            import numpy as np
            region = self.region
            frame = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region, allScreens=True)), cv2.COLOR_RGB2BGR)
            processed_frame = self.processor.process_frame(frame)
            return processed_frame

    def run(self):
        self.is_running = True

        if self.capture_mode == 0:
            self.run_webcam()
        elif self.capture_mode == 1:
            self.run_screen()

    def run_screen(self):
        FRAME_RATE = 60
        SLEEP_TIME = 1 / FRAME_RATE

        self.capture = self.WindowCapture(region=self.capture_area, capture_rate=FRAME_RATE, processor=self)
        
        # 가상 웹캠 설정
        height, width, _ = self.capture.frame.shape
        if self.virtual_cam_backend:
            with pyvirtualcam.Camera(width=width, height=height, fps=FRAME_RATE, backend=self.virtual_cam_backend, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
                self.run_screen_process(SLEEP_TIME, cam)
        else:
            self.run_screen_process(SLEEP_TIME)


    def run_screen_process(self, sleep_time , cam : pyvirtualcam.Camera = None):
        while self.is_running:
            start = time.time()
            processed_frame = self.capture.screenshot()
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.frame_ready.emit(q_img)  # 프레임을 GUI로 전송

            delta = time.time() - start
            if delta < sleep_time:
                time.sleep(sleep_time - delta)

            if self.is_record:
                self.output_video.write(processed_frame)

        # 종료 후 프레임 비우기
        self.frame_ready.emit(None)

    def run_webcam(self):
        if self.video_cap is None:
            self.video_cap = cv2.VideoCapture(self.current_webcam)
        
        if not self.video_cap.isOpened():
            print("Error: Could not open webcam.")
            return
        self.webcam_start.emit()
        height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        if self.virtual_cam_backend:
            with pyvirtualcam.Camera(width=width, height=height, fps=30, backend=self.virtual_cam_backend, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
                self.run_webcam_process(cam)
        else:
            self.run_webcam_process()

    def run_webcam_process(self, cam : pyvirtualcam.Camera= None):
        while self.is_running and self.video_cap.isOpened():
            self.webcam_on = True
            ret, frame = self.video_cap.read()  # 웹캠에서 프레임 읽기
            if ret:
                processed_frame = self.process_frame(frame)  # 프레임 처리
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환

                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(q_img)  # 프레임을 GUI로 전송

                # 가상 웹캠으로 프레임 전송
                if cam:
                    cam.send(processed_frame)
                    cam.sleep_until_next_frame()

                # 녹화
                if self.is_record:
                    self.output_video.write(processed_frame)

        # 종료 후 프레임 비우기
        self.frame_ready.emit(None)


    def process_frame(self, frame):
        '''프레임 처리 메서드 - 얼굴 모자이크 및 객체 인식'''
        processed_frame = frame
        if self.filtering.current_filter_info is not None:
            if self.filtering.current_filter_info.background_blur:
                processed_frame = self.filtering.background_blur(frame)
        boxesList = self.filtering.filtering(processed_frame, focus_area=self.focus_detection_area)
        for key in boxesList.keys():
            if key == -1:
                if boxesList[key] is not None:
                    processed_frame = self.filtering.blur(processed_frame, boxesList[key])
            elif key == -2:
                if boxesList[key] is not None:
                    processed_frame = self.filtering.square_blur(processed_frame, boxesList[key])
            elif key != -3:
                if boxesList[key] is not None:
                    processed_frame = self.filtering.face_sticker(processed_frame, boxesList[key], key)
    
        return processed_frame

    def set_filter(self, filter):
        """필터 설정"""
        if filter is not None:
            current_filter = self.filter_manager.get_filter(filter)
            self.filtering.set_filter(current_filter)
        else:
            self.filtering.set_filter(None)

    def pause(self):
        '''스레드 일시 중지'''
        if self.is_record:
            self.is_record = False
            self.output_video.release()
        self.is_running = False
        self.filtering.tracking_id_init()
        self.wait()

    def stop(self):
        '''스레드 종료 메서드'''
        if self.is_record:
            self.is_record = False
            self.output_video.release()
        self.is_running = False
        self.filtering.tracking_id_init()
        self.quit()
        if self.video_cap is not None:
            self.video_cap.release()
        self.video_cap = None

    def set_capture_area(self):
        if self.isRunning():
            self.pause()  # 스레드가 실행 중이면 중지
        
        app = DragArea.BlockClicksWindow()
        DragArea.create_window_on_each_display(app)
        app.start_event_handling()
        app.run()
        
        x1,y1,x2,y2 = app.clicked_coordinates
        w = abs(x1-x2) 
        h = abs(y1-y2)
        if (w == 0) | (h == 0):
            return
        self.capture_mode = 1
        self.del_focus_area()
        self.capture_area = (min(x1,x2),min(y1,y2), w, h)
        # print("Clicked coordinates:", self.capture_area)
        self.screen_size.emit((self.capture_area[2], self.capture_area[3]))

    def set_web_cam(self, web_cam):
        '''웹캠 설정'''
        isRunning = self.isRunning()
        if self.isRunning():
            self.pause()  # 스레드가 실행 중이면 중지
        self.set_webcam_mode()
        if self.current_webcam != web_cam:  # 새로운 웹캠이 이전과 다를 경우에만 설정 변경
            if self.video_cap is not None:
                self.video_cap.release()  # 이전 웹캠 해제
            self.video_cap = cv2.VideoCapture(web_cam)  # 새로운 웹캠 연결
            self.current_webcam = web_cam  # 현재 연결된 웹캠 번호 업데이트

        if isRunning:
            self.start()  # 스레드를 다시 시작

    def recordOn(self):
        if not self.isRunning():
            raise Exception("녹화를 위한 촬영이 진행되고 있지 않습니다")
        if self.capture_mode == 0:
            cap = self.video_cap
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = 20
        else:
            cap = self.capture
            frame_width = int(self.capture_area[2])
            frame_height = int(self.capture_area[3])
            fps = 20
        if cap is None:
            raise Exception("녹화에 대한 입력이 없습니다")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        video_name = f"output_video_{current_time}.mp4"
        self.video_path = self.path_manager.load_download_path()
        self.video_path = os.path.join(self.video_path, "Recodes", video_name)
        self.output_video = cv2.VideoWriter(self.video_path, fourcc, fps, (frame_width, frame_height))
        self.is_record = True
        
    def recordOff(self):
        if self.is_record:
            self.is_record = False
            self.output_video.release()

    def set_webcam_mode(self):
        self.del_focus_area()
        self.capture_mode = 0

    def set_focus_area(self, box):
        """box의 좌표는 x1, y1, x2, y2의 형식이다"""
        if box[0] == 0 and box[1] == 0 and box[2] == 0 and box[3] == 0:
            self.focus_detection_area = None
            return
        self.focus_detection_area = box

    def del_focus_area(self):
        self.focus_detection_area = None
