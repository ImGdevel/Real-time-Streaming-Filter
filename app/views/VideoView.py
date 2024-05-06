from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QHBoxLayout, QSizePolicy, QFrame, QProgressDialog
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtCore import Qt, QThread, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from controllers import VideoProcessor
from views.component import FilterListWidget, VideoPlayer, ShadowWidget, SettingWidget, ContentLabeling
from utils import Colors, Style, Icons

class VideoView(QWidget):
    '''PySide6를 이용한 비디오 재생 화면 구성 클래스'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_processor = VideoProcessor()
        self.video_processor.encodingVideoPathEvent.connect(self.get_encoding_video)
        self.origin_video_path : str = None
        self.encoding_video_path : str = None
        self.initUI()

    def initUI(self):
        '''UI 초기화'''
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        self.video_player = VideoPlayer()
        self.video_player.setPlayVideo.connect(self.get_encoding_video)
        

        
        self.setting_widget = SettingWidget()
        self.setting_widget.setStyleSheet(Style.frame_style)
        self.setting_widget.setGraphicsEffect(Style.shadow(self.setting_widget))
        self.setting_widget.setMinimumWidth(200)
        self.setting_widget.setMaximumWidth(240)
        # 설정 위젯에 버튼 추가
        self.initSettingButtons()
        
        layout.addWidget(self.video_player, 4)
        layout.addWidget(self.setting_widget, 1)

        self.setLayout(layout)

    def initSettingButtons(self):
        '''설정 위젯에 버튼 추가'''

        list_frame = ContentLabeling()
        list_frame.setLabel("필터 목록")
        list_frame.setStyleSheet(Style.frame_style)
        list_frame.setContentMargin(10,10,10,10)
        
        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.set_items_event(self.set_filter_option)
        list_frame.setContent(self.filter_list_widget)
        

        self.button1 = QPushButton("Encoding")
        self.button1.setFixedHeight(40)
        self.button1.clicked.connect(self.do_video_encoding)
        self.button2 = QPushButton("Download")
        self.button2.setFixedHeight(40)
        self.button2.clicked.connect(self.download_video)
        self.button3 = QPushButton()
        self.button3.setIcon(QIcon(Icons.folder_open))
        self.button3.clicked.connect(self.openFileDialog)
        self.button3.setFixedSize(50, 50)

        self.setting_widget.addSettingButton(self.button3)
        self.setting_widget.addWidget(list_frame)
        self.setting_widget.addSettingButton(self.button1)
        self.setting_widget.addSettingButton(self.button2)
        
    
    
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
        #다이얼로그 구문 
        progress_dialog = QProgressDialog("Encoding", "Cancel", 0, 100)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()
        self.video_processor.filtering_video(self.origin_video_path, progress_dialog)
        
    def get_encoding_video(self, video_path):
        """인코딩 후 영상 반환, 재생"""
        print("인코딩 영상 재생!!")
        self.encoding_video_path = video_path
        self.play_video(video_path)
    
    def download_video(self):
        """영상 다운로드"""
        self.video_processor.download_video()
        
    def render(self):
        """페이지 refresh"""
        self.filter_list_widget.update_list()
        
