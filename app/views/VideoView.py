import os
import cv2
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QHBoxLayout, QSizePolicy, QFrame
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtCore import Qt, QThread, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from .component import SettingWidget
from controllers import VideoProcessor
from views.component import FilterListWidget
from views.component import VideoPlayer

class VideoInfo:
    '''비디오 파일 정보를 관리하는 클래스'''
    def __init__(self, video_path):
        self.video_path = video_path
        self.video_name = os.path.basename(video_path)
        self.video_extension = os.path.splitext(video_path)[1][1:].lower()
        self.video_size = os.path.getsize(video_path)

class VideoView(QWidget):
    '''PySide6를 이용한 비디오 재생 화면 구성 클래스'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_processor = VideoProcessor()
        self.video_path = str
        self.initUI()

    def initUI(self):
        '''UI 초기화'''
        self.layout = QHBoxLayout()
        self.initVideoWidget()
        self.initSettingWidget()
        self.setLayout(self.layout)

    def render(self):
        """페이지 refresh"""
        self.filter_list_widget.update_filter_list()

    def initVideoWidget(self):
        '''비디오 위젯 및 레이아웃 초기화'''
        self.video_Player = VideoPlayer()
        self.layout.addWidget(self.video_Player)
        self.layout.setAlignment(Qt.AlignCenter)  # 부모 위젯의 레이아웃을 가운데 정렬로 설정

    def initSettingWidget(self):
        '''설정 위젯 초기화'''
        self.setting_widget = SettingWidget()
        self.setting_widget.Encoding_button.clicked.connect(self.inCoding)
        self.setting_widget.setMinimumWidth(200)
        self.setting_widget.setMaximumWidth(240)
        # 설정 위젯에 버튼 추가
        self.initSettingButtons()
        
        self.layout.addWidget(self.setting_widget)

    def initSettingButtons(self):
        '''설정 위젯에 버튼 추가'''

        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.onClickItemEvent.connect(self.set_filter_option)

        self.button1 = QPushButton("Test - 인코딩")
        self.button1.clicked.connect(self.button1Act)
        self.button2 = QPushButton("Test - download")
        self.button2.clicked.connect(self.button2Act)
        self.button3 = QPushButton("Test - VideoUpload")
        self.button3.clicked.connect(self.button3Act)

        self.setting_widget.addWidget(self.filter_list_widget)
        self.setting_widget.addSettingButton(self.button1)
        self.setting_widget.addSettingButton(self.button2)
        self.setting_widget.addSettingButton(self.button3)
    
    def button3Act(self):
        self.openFileDialog()
        

    def set_filter_option(self, index):
        """필터 옵션 선택"""
        self.video_processor.set_filter(index)


    def openFileDialog(self):
        '''파일 대화상자를 통해 비디오 파일 선택'''
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.video_Player.set_video(filePath)
            self.video_Player.start_video()


    def updateVideoFrame(self, frame):
        '''비디오 프레임을 QLabel 위젯에 업데이트'''
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_frame.shape
        q_img = QImage(rgb_frame.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_widget.setPixmap(pixmap.scaled(self.video_widget.width(), self.video_widget.height()))


    def updateVideoBar(self, current_frame_num):
        '''비디오 슬라이더의 위치 업데이트'''
        total_frames = self.video_processor.video_frame_count
        value = int((current_frame_num / total_frames) * 100)
        self.video_bar.setValue(value)
        
        # FPS 가져오기
        fps = self.video_processor.fps
        current_time = self.convertTime(current_frame_num, total_frames, fps)
        
        # 비디오 바 왼쪽에 현재 재생 시간 표시
        self.video_bar.setTickInterval(1)  # 틱 간격을 1로 설정
        self.video_bar.setTickPosition(QSlider.TicksBothSides)  # 틱 위치 설정
        self.video_bar.setToolTip(current_time)  # 툴팁으로 현재 시간 표시

        # 현재 재생 시간 레이블 업데이트
        self.current_time_label.setText(current_time)


    def updateFPSLabel(self, fps_value):
        '''FPS 레이블 업데이트'''
        self.fps_label.setText(f"FPS: {fps_value}")


    def openFileDialogOnClick(self, event):
        '''파일 대화상자를 통해 비디오 파일 선택 (마우스 클릭 이벤트로 트리거)'''
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.loadVideo(filePath)


    def dragEnterEvent(self, event: QDragEnterEvent):
        '''드래그 이벤트 오버라이드'''
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event: QDropEvent):
        '''드롭 이벤트 오버라이드'''
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            file_path = files[0]  # 첫 번째 파일만 가져옴
            self.loadVideo(file_path)


    def loadVideo(self, file_path):
        '''비디오 파일 로드'''
        self.video_path = file_path
        self.video_info = VideoInfo(file_path)
        self.video_processor.set_video(file_path)
        self.video_processor.video_frame.connect(self.updateVideoFrame)
        self.video_processor.current_frame.connect(self.updateVideoBar)
        self.video_processor.fps_signal.connect(self.updateFPSLabel)  # FPS 신호 연결
        self.video_processor.start()


    def pauseVideo(self):
        '''비디오 일시정지'''
        if hasattr(self, 'video_processor') and self.video_processor.is_video_ready:
            self.video_processor.terminate()


    def stopVideo(self):
        '''비디오 정지'''
        if hasattr(self, 'video_processor') and self.video_processor.is_video_ready:
            self.video_processor.terminate()
            self.video_processor.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상의 시작 지점으로 이동
            self.video_bar.setValue(0)  # 슬라이더 값도 초기화


    def convertTime(self, frame_number, total_frames, fps):
        '''프레임 번호를 시간 형식으로 변환'''
        if fps == 0:
            return "00:00:00"  # fps 값이 0일 경우 "00:00:00"을 반환하여 오류를 방지
        seconds = frame_number / fps
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    def inCoding(self):
        path = self.video_path
        print(path)

    def button1Act(self):
        print("인코딩 실행")
        self.video_processor.filtering_video()
    
    def button2Act(self):
        self.video_processor.download_video()
        
