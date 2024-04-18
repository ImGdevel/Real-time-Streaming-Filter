import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from models import Filtering, FilterManager

class VideoProcessor(QThread):
    '''비디오 재생을 위한 스레드 클래스'''
    video_frame = pyqtSignal(object)  # 비디오 프레임 신호
    current_frame = pyqtSignal(int)    # 현재 프레임 신호
    fps_signal = pyqtSignal(float)     # FPS 신호

    def __init__(self, video_path):
        super(VideoProcessor, self).__init__()
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.video_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))  # FPS 값 가져오기
        self.is_playing = True
        self.filtering = Filtering()

    def run(self):
        '''비디오 재생 스레드의 메인 루프'''
        while self.cap.isOpened() and self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                current_frame_num = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.video_frame.emit(frame)        # 비디오 프레임 신호 발생
                self.current_frame.emit(current_frame_num)  # 현재 프레임 신호 발생
                self.fps_signal.emit(self.fps)      # FPS 신호 발생
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
                
        self.cap.release()




    # 동영상 받아서 필터링된 동영상 파일 임시 생성
    def filtering_video(self):
        cap = cv2.VideoCapture(self.video_path) #filtered video_path
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 새 동영상 파일 경로 및 설정
        output_video_path = 'output_video.mp4'

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        while True:
            ret, frame = cap.read()  # 프레임 읽기
            if not ret:
                break  # 동영상 끝에 도달하면 반복 중지

            # 여기서 프레임 처리 (예: 필터링, 객체 감지 등)
            blur_ratio = 50
        
            testDict = dict()
            obj = self.filtering.object
            for cls in obj.orgNames:
                testDict[obj.orgNames[cls]] = 0
            for cls in obj.custNames:
                testDict[obj.custNames[cls]] = 1
            testDict["Human face"] = 1
            
            boxesList = self.filtering.filtering(frame, testDict)
            processed_frame = self.filtering.blur(blur_ratio, frame, boxesList)
            # 출력 동영상에 프레임 쓰기
            output_video.write(processed_frame)

        cap.release()
        cv2.destroyAllWindows()


    def run_filtered_video(self):
        '''필터링된 비디오 재생'''
        filtered_cap = cv2.VideoCapture('output_video.mp4') #링크는 나중에 바꾸고
        while filtered_cap.isOpened() and self.is_playing:
            ret, frame = filtered_cap.read()
            if ret:
                current_frame_num = int(filtered_cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.video_frame.emit(frame)        # 비디오 프레임 신호 발생
                self.current_frame.emit(current_frame_num)  # 현재 프레임 신호 발생
                self.fps_signal.emit(self.fps)      # FPS 신호 발생
            else:
                filtered_cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
                
        filtered_cap.release()