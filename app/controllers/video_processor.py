from datetime import datetime
import os
import time
import cv2
import shutil
from PySide6.QtCore import QThread, Signal
from models import Filtering, FilterManager, PathManager
from PySide6.QtWidgets import QApplication

class VideoProcessor(QThread):
    '''비디오 재생을 위한 스레드 클래스'''
    encodingVideoPathEvent = Signal(str) # 인코딩된 영상 path
    progressChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.filtering = Filtering()
        self.filter_manager = FilterManager()
        self.path_manager = PathManager()
        self.temp_video_path : str = None
        self.video_path : str = None
        self.is_running : bool = False
        self.origin_video_path : str = None
        self.is_complete = True

    def run(self):
        self.filtering_video(self.origin_video_path)
        
    def set_video(self, video_path):
        self.video_path = video_path

    def set_origin_video(self, origin_video_path):
        self.origin_video_path = origin_video_path
        
    # 동영상 받아서 필터링된 동영상 파일 임시 생성
    def filtering_video(self, video_path):

        self.is_complete = False
        cap = cv2.VideoCapture(video_path) #filtered video_path
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_elements = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 새 동영상 파일 경로 및 설정
        self.temp_video_path = os.path.join(self.path_manager.load_TempData_path(),'output_video.mp4')
        
        # 파일 존재 여부 확인 및 삭제
        if os.path.exists(self.temp_video_path):
            os.remove(self.temp_video_path)

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video = cv2.VideoWriter(self.temp_video_path, fourcc, fps, (frame_width, frame_height))

        i = 0
        self.filtering.tracking_id_init()

        self.is_running = True
        while self.is_running:
            #작업 진행상황 업데이트
            progress = ((i) / total_elements) * 100
            self.progressChanged.emit(progress)

            ret, frame = cap.read()  # 프레임 읽기            
            if not ret:
                self.is_complete = True
                break  # 동영상 끝에 도달하면 반복 중지

            processed_frame = self.process_frame(frame)
            output_video.write(processed_frame)
            i += 1

        output_video.release()
        cap.release()
        cv2.destroyAllWindows()
        if self.is_complete is True:
            self.encodingVideoPathEvent.emit(self.temp_video_path)
        else:
            self.is_complete = True




    def process_frame(self, frame):
        '''프레임 처리 메서드 - 얼굴 모자이크 및 객체 인식'''
        processed_frame = frame
        if self.filtering.current_filter_info is not None:
            if self.filtering.current_filter_info.background_blur:
                processed_frame = self.filtering.background_blur(processed_frame)
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
    

    def encoding_cancel(self):
        self.is_running = False
        if self.isRunning():
            self.wait()
        
    def download_video(self):
        """필터링 된 비디오를 다운합니다."""
        # todo : output_video_path를 다운로드 경로로 이동
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        video_name = f"output_video_{current_time}.mp4"
        output_video_path = self.path_manager.load_download_path()
        output_video_path = os.path.join(output_video_path, "videos", video_name)
        if self.temp_video_path is None:
            raise ValueError("인코딩된 동영상이 존재하지 않습니다.")
        else:
            shutil.copy(self.temp_video_path, output_video_path)
            print("copy video to : " + output_video_path)
            return output_video_path
        
    def set_filter(self, filter):
        """필터 설정"""
        if not filter is None:
            current_filter = self.filter_manager.get_filter(filter)
            #print("현제 적용 필터 :",  current_filter)
            self.filtering.change_filter(current_filter)
            