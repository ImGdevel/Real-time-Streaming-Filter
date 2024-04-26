import cv2
import shutil
from PySide6.QtCore import QThread, Signal
from models import Filtering, FilterManager, PathManager

class VideoProcessor(QThread):
    '''비디오 재생을 위한 스레드 클래스'''
    encodingVideoPathEvent = Signal(str) # 인코딩된 영상 path

    def __init__(self):
        super().__init__()
        self.filtering = Filtering()
        self.filter_manager = FilterManager()
        self.path_manager = PathManager()
        self.temp_video_path = str
        self.current_filter = None
        
    # 동영상 받아서 필터링된 동영상 파일 임시 생성
    def filtering_video(self, vidoe_path):

        cap = cv2.VideoCapture(vidoe_path) #filtered video_path
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 새 동영상 파일 경로 및 설정
        self.temp_video_path = 'output_video.mp4'

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video = cv2.VideoWriter(self.temp_video_path, fourcc, fps, (frame_width, frame_height))

        while True:
            ret, frame = cap.read()  # 프레임 읽기
            if not ret:
                break  # 동영상 끝에 도달하면 반복 중지

            
            boxesList = self.filtering.filtering(frame, self.current_filter)
            processed_frame = self.filtering.replace_face_img(frame, boxesList, -1)
            # 출력 동영상에 프레임 쓰기
            output_video.write(processed_frame)

        cap.release()
        cv2.destroyAllWindows()
        print("인코딩 완료")
        self.encodingVideoPathEvent.emit(self.temp_video_path)
        
    def download_video(self):
        """필터링 된 비디오를 다운합니다."""
        # todo : output_video_path를 다운로드 경로로 이동
        self.output_video_path = self.path_manager.load_download_path()
        shutil.move(self.temp_video_path, self.output_video_path)
        print("move video to : " + self.output_video_path)
        
    def set_filter(self, filter):
        """필터 설정"""
        if not filter is None:
            self.current_filter = self.filter_manager.get_filter(filter)
            print("현제 적용 필터 :",  self.current_filter)