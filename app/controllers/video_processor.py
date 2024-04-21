import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from models import Filtering, FilterManager, PathManager
import shutil

class VideoProcessor(QThread):
    '''비디오 재생을 위한 스레드 클래스'''
    video_frame = pyqtSignal(object)  # 비디오 프레임 신호
    current_frame = pyqtSignal(int)    # 현재 프레임 신호
    fps_signal = pyqtSignal(float)     # FPS 신호

    def __init__(self):
        super().__init__()
        self.filtering = Filtering()
        self.filter_manager = FilterManager()
        #임시 경로와 다운로드 할 경로
        self.path_manager = PathManager()

        self.temp_video_path = str
        
        self.current_filter = None
        self.is_playing = False
        self.is_video_ready = False

    def set_video(self, video_path):
        """재생할 비디오를 세팅합니다"""
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path) # 재생할 비디오 캡쳐
        self.video_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 비디오 카운터 (재생위치 조절)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))  # FPS 값 가져오기 
        self.is_video_ready = True

    def run(self):
        self.is_playing = True
        '''비디오 재생 스레드의 메인 루프'''
        while self.is_playing and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                current_frame_num = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) # 현재 재생 위치
                self.video_frame.emit(frame)        # 비디오 프레임 신호 발생
                self.current_frame.emit(current_frame_num)  # 현재 프레임 신호 발생
                self.fps_signal.emit(self.fps)      # FPS 신호 발생
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.cap.release()
    
    def play_video(self):
        """비디오를 재생합니다"""
        if self.is_video_ready:
            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.video_frame_count:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상의 시작 지점으로 이동
            self.start()
        else:
            print("비디오가 없습니다.")

    def puse_video(self):
        """비디오를 일시정지 합니다"""

        pass

    # 동영상 받아서 필터링된 동영상 파일 임시 생성
    def filtering_video(self):
        cap = cv2.VideoCapture(self.video_path) #filtered video_path
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

            # 여기서 프레임 처리 (예: 필터링, 객체 감지 등)
            #blur_ratio = 50
    
            
            boxesList = self.filtering.filtering(frame, self.current_filter)
            processed_frame = self.filtering.blur(frame, boxesList)
            # 출력 동영상에 프레임 쓰기
            output_video.write(processed_frame)

        cap.release()
        cv2.destroyAllWindows()
        print("인코딩 완료")
        self.set_video(self.temp_video_path) # 필터된 비디오로 재생 연결
        self.play_video()

    def download_video(self):
        """필터링 된 비디오를 다운합니다."""
        # todo : output_video_path를 다운로드 경로로 이동
        
        self.output_video_path = self.path_manager.load_download_path()
        shutil.move(self.temp_video_path, self.output_video_path)
        print("move video to : " + self.output_video_path)

        pass
        
    def set_filter(self, filter):
        """필터 설정"""
        if not filter is None:
            self.current_filter = self.filter_manager.get_filter(filter)
            print("현제 적용 필터 :",  self.current_filter)