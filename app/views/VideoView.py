from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QHBoxLayout, QSizePolicy, QFrame
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtCore import Qt, QThread, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from .component import SettingWidget
from controllers import VideoProcessor
from views.component import FilterListWidget
from views.component import VideoPlayer

class VideoView(QWidget):
    '''PySide6를 이용한 비디오 재생 화면 구성 클래스'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_processor = VideoProcessor()
        self.origin_video_path : str = None
        self.encoding_video_path : str = None
        self.initUI()

    def initUI(self):
        '''UI 초기화'''
        self.layout = QHBoxLayout()
        self.initVideoWidget()
        self.initSettingWidget()
        self.setLayout(self.layout)

    def initVideoWidget(self):
        '''비디오 위젯 및 레이아웃 초기화'''
        self.video_player = VideoPlayer()
        self.video_player.setPlayVideo.connect(self.get_encoding_video)
        self.layout.addWidget(self.video_player)
        self.layout.setAlignment(Qt.AlignCenter)  # 부모 위젯의 레이아웃을 가운데 정렬로 설정

    def initSettingWidget(self):
        '''설정 위젯 초기화'''
        self.setting_widget = SettingWidget()
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
        self.button1.clicked.connect(self.do_video_encoding)
        self.button2 = QPushButton("Test - download")
        self.button2.clicked.connect(self.download_video)
        self.button3 = QPushButton("Test - VideoUpload")
        self.button3.clicked.connect(self.openFileDialog)

        self.setting_widget.addWidget(self.filter_list_widget)
        self.setting_widget.addSettingButton(self.button1)
        self.setting_widget.addSettingButton(self.button2)
        self.setting_widget.addSettingButton(self.button3)
    
    


    def openFileDialog(self):
        '''파일 대화상자를 통해 비디오 파일 선택'''
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.origin_video_path = filePath
            self.play_video(filePath)
        
    def play_video(self, video_path):
        """영상 재생"""
        self.video_player.set_video(video_path)
        self.video_player.start_video()

    def set_filter_option(self, index):
        """필터 옵션 선택"""
        self.video_processor.set_filter(index)

    def do_video_encoding(self):
        """비디오 인코딩"""
        self.video_processor.filtering_video(self.origin_video_path)
        
    def get_encoding_video(self, video_path):
        """인코딩 후 영상 반환, 재생"""
        self.encoding_video_path = video_path
        self.play_video(video_path)
    
    def download_video(self):
        """영상 다운로드"""
        self.video_processor.download_video()
        
    def render(self):
        """페이지 refresh"""
        self.filter_list_widget.update_filter_list()
        
