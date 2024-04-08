from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl
from utils import Colors
from contollers.video_player_thread import VideoPlayerThread

class VideoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QGridLayout()

        # 비디오 영역
        self.right_widget = QWidget()
        self.right_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.right_widget.setMinimumWidth(300)
        self.layout.addWidget(self.right_widget, 0, 0, 1, 1)

        self.video_layout = QVBoxLayout()
        self.right_widget.setLayout(self.video_layout)

       # 비디오 위젯 추가
        self.video_widget = QLabel(self)
        self.video_widget.setFixedSize(640, 480)  # 비디오 크기 설정
        self.video_layout.addWidget(self.video_widget)

        # 파일 탐색기 버튼
        self.file_dialog_button = QPushButton("Choose Video File")
        self.file_dialog_button.clicked.connect(self.openFileDialog)
        self.video_layout.addWidget(self.file_dialog_button)

        # video 바
        self.video_bar = QWidget()
        self.video_bar.setStyleSheet(f'background-color: {Colors.baseColor02};')
        self.video_bar.setMaximumHeight(15)
        self.video_layout.addWidget(self.video_bar)

        # 메뉴 영역
        self.remaining_widget = QWidget()
        self.remaining_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.remaining_widget.setFixedWidth(150)
        self.layout.addWidget(self.remaining_widget, 0, 1, 1, 1)

        self.setLayout(self.layout)

    def openFileDialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi);;All Files (*)", options=options)
        if filePath:
            self.video_thread = VideoPlayerThread(filePath, self.video_widget)
            self.video_thread.start()