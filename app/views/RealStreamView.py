from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,  QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,  QTimer
from utils import Colors
from contollers import VideoProcessor

from contollers import RealStreamProcessor

class RealStreamView(QWidget):
    """실시간 스트리밍 View"""
    """실시간 스트리밍 View"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        '''GUI 초기화 메서드'''
        self.layout = QGridLayout()  # 레이아웃 설정
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setup_toolbar()  # 툴바 설정
        self.setup_video_layer()  # 비디오 레이어 설정
        self.setup_bottom_layer()  # 하단 레이어 설정

        self.setLayout(self.layout)

        self.video_processor = RealStreamProcessor()  # 실시간 영상 처리 스레드 객체 생성
        self.video_processor.frame_ready.connect(self.update_video)  # 프레임 수신 시 GUI 업데이트 연결
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)

    def setup_toolbar(self):
        '''툴바 설정 메서드'''
        self.toolbar = QWidget()  # 툴바 위젯
        self.toolbar.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 배경색 설정
        self.toolbar.setFixedSize(300, 450)  # 크기 설정
        self.layout.addWidget(self.toolbar, 0, 0)

        # 툴바에 버튼 추가
        self.toggle_button = QPushButton("Toggle Webcam")  # 웹캠 토글 버튼
        self.toggle_button.setCheckable(True)  # 체크 가능 설정
        self.toggle_button.clicked.connect(self.toggle_webcam)  # 클릭 이벤트 연결

        self.flip_button = QPushButton("Flip Horizontal")  # 화면 좌우 뒤집기 버튼
        self.flip_button.clicked.connect(self.flip_horizontal)  # 클릭 이벤트 연결

        self.mosaic_button = QPushButton("Toggle Mosaic")  # 모자이크 토글 버튼
        self.mosaic_button.setCheckable(True)  # 체크 가능 설정
        self.mosaic_button.clicked.connect(self.toggle_mosaic)  # 클릭 이벤트 연결

        # 툴바에 버튼 배치
        toolbar_layout = QVBoxLayout()
        toolbar_layout.addWidget(self.toggle_button)
        toolbar_layout.addWidget(self.flip_button)
        toolbar_layout.addWidget(self.mosaic_button)
        self.toolbar.setLayout(toolbar_layout)

    def setup_video_layer(self):
        '''비디오 레이어 설정 메서드'''
        self.video_widget = QLabel()  # 비디오 플레이어 레이블
        self.video_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 배경색 설정
        self.video_widget.setAlignment(Qt.AlignCenter)  # 정렬 설정
        self.layout.addWidget(self.video_widget, 0, 1)

    def setup_bottom_layer(self):
        '''하단 레이어 설정 메서드'''
        self.bottom_widget = QWidget()  # 하단 위젯
        self.bottom_layout = QVBoxLayout()  # 수직 레이아웃
        self.bottom_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 배경색 설정
        self.bottom_widget.setLayout(self.bottom_layout)

        self.layout.addWidget(self.bottom_widget, 1, 0, 1, 2)

    def toggle_webcam(self):
        '''웹캠 토글 메서드'''
        if self.toggle_button.isChecked():
            if not self.video_processor.isRunning():
                self.video_processor.start()
                self.toggle_button.setText("Stop Webcam")
                self.timer.start(0)  # 비동기적으로 프레임 업데이트
        else:
            if self.video_processor.isRunning():
                self.video_processor.stop()
                self.toggle_button.setText("Start Webcam")
                self.timer.stop()

    def flip_horizontal(self):
        '''화면 좌우 뒤집기 메서드'''
        self.video_processor.flip_horizontal()

    def toggle_mosaic(self):
        '''모자이크 토글 메서드'''
        if self.mosaic_button.isChecked():
            # 모자이크 활성화
            self.video_processor.mosaic_active = True
            self.mosaic_button.setText("Disable Mosaic")
        else:
            # 모자이크 비활성화
            self.video_processor.mosaic_active = False
            self.mosaic_button.setText("Toggle Mosaic")

    def update_video(self, q_img=None):
        '''비디오 업데이트 메서드'''
        if q_img is None:
            return
        pixmap = QPixmap.fromImage(q_img)
        self.video_widget.setPixmap(pixmap.scaled(self.video_widget.width(), self.video_widget.height(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
        '''GUI 종료 이벤트 메서드'''
        self.video_processor.stop()
        self.timer.stop()
