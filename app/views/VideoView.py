import time
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QHBoxLayout, QSizePolicy, QFrame, QProgressDialog, QMessageBox
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtCore import Qt, QThread, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from controllers import VideoProcessor
from views.component import FilterListWidget, VideoPlayer, SettingWidget, ContentLabeling
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
        
        right_layout = QWidget()
        
        # 설정 위젯에 버튼 추가
        left_layout = self.initSettingButtons()
        
        layout.addWidget(self.video_player, 4)
        layout.addWidget(left_layout, 1)

        self.setLayout(layout)

    def initSettingButtons(self):
        '''설정 위젯에 버튼 추가'''
        frame = QWidget()
        frame.setStyleSheet(Style.frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        frame.setMinimumWidth(200)
        
        setting_widget = SettingWidget()
        
        list_frame = ContentLabeling()
        list_frame.setLabel("필터 목록")
        list_frame.setStyleSheet(Style.frame_style)
        list_frame.setContentMargin(0,0,0,0)
        
        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.set_items_event(self.set_filter_option)
        list_frame.setContent(self.filter_list_widget)

        self.button1 = QPushButton("인코딩")
        self.button1.setFixedHeight(40)
        self.button1.setStyleSheet(Style.mini_button_style)
        self.button1.clicked.connect(self.do_video_encoding)
        self.button2 = QPushButton("다운로드")
        self.button2.setStyleSheet(Style.mini_button_style)
        self.button2.setFixedHeight(40)
        self.button2.clicked.connect(self.download_video)
        self.button3 = QPushButton()
        self.button3.setIcon(QIcon(Icons.folder_open))
        self.button3.clicked.connect(self.openFileDialog)
        self.button3.setFixedSize(50, 50)
        self.button3.setToolTip("파일탐색")
        setting_widget.addWidget(list_frame)

        setting_button_layout = QVBoxLayout()
        setting_button_frame = QWidget()
        setting_button_layout.setContentsMargins(15,0,15,5)
        setting_button_layout.addWidget(self.button1)
        setting_button_layout.addWidget(self.button2)
        setting_button_frame.setLayout(setting_button_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.button3)
        layout.addWidget(setting_widget)
        layout.addWidget(setting_button_frame)
        layout.setContentsMargins(5,5,5,5)
        frame.setLayout(layout)
        return frame
        
    def openFileDialog(self):
        '''파일 대화상자를 통해 비디오 파일 선택'''
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.origin_video_path = filePath
            self.video_processor.set_origin_video(filePath)
            self.video_processor.is_complete = True
            self.play_video(filePath)

    def play_video(self, video_path):
        """영상 재생"""
        if self.video_processor.is_complete is True :
            self.video_processor.set_video(video_path)
            self.video_player.set_video(video_path)
            self.video_player.start_video()
        else :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("영상파일을 인식할 수 없습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()

    def set_filter_option(self, index):
        """필터 옵션 선택"""
        self.video_processor.set_filter(index)

    def do_video_encoding(self):
        """비디오 인코딩"""
        #다이얼로그 구문 
        print("do_video_encoding")
        if self.origin_video_path:
            self.progress_dialog = QProgressDialog("Encoding", "Cancel", 0, 100)
            self.video_processor.progressChanged.connect(self.setProgress)
            self.progress_dialog.canceled.connect(self.cancelCounting) # 취소시

            self.video_player.pause_video()

            self.video_processor.start()

            #self.progress_dialog.exec_()
            
        else:
            # todo : 동영상이 선택 되지 않았음을 알려야 함
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("등록된 영상파일이 존재하지 않습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()
    
    def setProgress(self, value):
        """작업 진행 상황 업데이트"""
        print("setProgress")
        self.progress_dialog.setValue(value)

    def cancelCounting(self):
        """인코딩 취소시"""
        self.video_processor.encoding_cancel()
        print("원래 비디오 재생할게요?")
        self.encoding_video_path = self.origin_video_path
        self.play_video(self.origin_video_path)
        
    def get_encoding_video(self, video_path):
        """인코딩 후 영상 반환, 재생"""
        print("get_encoding_video")
        if self.video_processor.is_complete is True :
            self.encoding_video_path = video_path
            self.play_video(video_path)

    
    def download_video(self):
        """영상 다운로드"""
        try:
            path = self.video_processor.download_video()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"다운로드가 완료되었습니다 \n{path}")
            msg.setWindowTitle("알림")
            msg.exec_()
        except ValueError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("인코딩 영상이 존재하지 않습니다")
            msg.setWindowTitle("경고")
            msg.exec_()
            
        
        
    def render(self):
        """페이지 refresh"""
        self.filter_list_widget.update_list()
        
    def swap_event(self):
        
        pass
        
