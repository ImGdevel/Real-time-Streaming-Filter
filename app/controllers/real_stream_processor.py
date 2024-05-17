from datetime import datetime
import cv2
from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import QThread, Signal
from models import Filtering, FilterManager, PathManager
from models import DragArea
import time, os



# 비디오 처리 스레드
class RealStreamProcessor(QThread):
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
        self.is_flipped = True  # 화면 좌우 뒤집기 상태
        self.webcam_on = False
        self.current_webcam = 0
        self.capture_mode = 0
        self.capture_area = None
        self.video_path : str = None
        self.is_record = False
        self.output_video = None
        
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
            frame = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=region, allScreens=True)), cv2.COLOR_RGB2BGR)
            
            processed_frame = self.processor.process_frame(frame)

            return processed_frame

    def run(self):
        self.is_running = True

        if self.capture_mode == 0:
            self.run_webcam()
        elif self.capture_mode == 1:
            self.run_screen()

        # 종료 후 프레임 비우기




    def run_screen(self):
        FRAME_RATE = 60
        SLEEP_TIME = 1/FRAME_RATE
        capture = self.WindowCapture(region=self.capture_area, capture_rate=FRAME_RATE, processor=self)

        height = None
        width = None
        
        self.capture = self.WindowCapture(region=self.capture_area, capture_rate=FRAME_RATE, processor=self)

        while self.is_running:
            start=time.time()
            processed_frame = self.capture.screenshot()
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.frame_ready.emit(q_img)  # 프레임을 GUI로 전송

            delta= time.time()-start
            if delta <SLEEP_TIME:
                time.sleep(SLEEP_TIME-delta)

            if self.is_record:
                self.output_video.write(processed_frame)

        if width != None & height != None:
            self.frame_clear(width, height)


    def run_webcam(self):
        if self.video_cap is None:
            self.video_cap = cv2.VideoCapture(self.current_webcam)
        
        height = None
        width = None

        while self.is_running and self.video_cap.isOpened():
            self.webcam_on = True
            #start = time.time()
            ret, frame = self.video_cap.read()  # 웹캠에서 프레임 읽기
            if ret:
                processed_frame = self.process_frame(frame)  # 프레임 처리
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환

                # if self.is_flipped:
                #     frame_rgb = cv2.flip(frame_rgb, 1)  # 화면 좌우 뒤집기

                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width
                q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(q_img)  # 프레임을 GUI로 전송

                if self.is_record:
                    self.output_video.write(processed_frame)
            #end = time.time()
            #result = end - start
            #print("time: "+ str(result))
        # 종료 후 프레임 비우기
        if width != None & height != None:
            self.frame_clear(width, height)



    def process_frame(self, frame):
        '''프레임 처리 메서드 - 얼굴 모자이크 및 객체 인식'''
        processed_frame = frame
        boxesList = self.filtering.filtering(frame)    
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
    
    def frame_clear(self, width, height):
        empty_frame = QImage(width, height, QImage.Format_RGB888)
        empty_frame.fill(QColor(23, 26, 30))
        self.frame_ready.emit(empty_frame)
        pass

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
        if self.is_record:
            self.is_record = False
            self.output_video.release()
        self.filtering.tracking_id_init()
        
        self.wait()

    def stop(self):
        '''스레드 종료 메서드'''
        self.is_running = False
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
        if w == 0 | h == 0:
            return
        self.capture_mode = 1
        self.capture_area = (min(x1,x2),min(y1,y2), w, h)
        print("Clicked coordinates:", self.capture_area)
        self.screen_size.emit((self.capture_area[2], self.capture_area[3]))



    def set_web_cam(self, web_cam):

        '''웹캠 설정'''
        if self.isRunning():
            self.pause()  # 스레드가 실행 중이면 중지
        print("set_web_cam")
        self.capture_mode = 0
        if self.current_webcam != web_cam:  # 새로운 웹캠이 이전과 다를 경우에만 설정 변경
            if self.video_cap is not None:
                self.video_cap.release()  # 이전 웹캠 해제
            self.video_cap = cv2.VideoCapture(web_cam)  # 새로운 웹캠 연결
            self.current_webcam = web_cam  # 현재 연결된 웹캠 번호 업데이트

        if self.isRunning():
            self.start()  # 스레드를 다시 시작

    def recordOn(self):
        if not self.isRunning():
            raise Exception("녹화를 위한 촬영이 진행되고 있지 않습니다")
        if self.capture_mode == 0:
            cap = self.video_cap
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.video_cap.get(cv2.CAP_PROP_FPS)
        else:
            cap = self.capture
            frame_width = int(self.capture_area[2])
            frame_height = int(self.capture_area[3])
            fps = 60
        if cap is None:
            raise Exception("녹화에 대한 입력이 없습니다")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        video_name = f"output_video_{current_time}.mp4"
        self.video_path = self.path_manager.load_download_path()
        self.video_path = os.path.join(self.video_path, video_name)
        self.output_video = cv2.VideoWriter(self.video_path, fourcc, fps, (frame_width, frame_height))
        self.is_record = True
    
    def set_webcam_mode(self):
        self.capture_mode = 0
