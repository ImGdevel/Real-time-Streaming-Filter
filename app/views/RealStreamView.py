from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QComboBox, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from utils import Colors
from controllers import RealStreamProcessor

class RealStreamView(QWidget):
    """실시간 스트리밍 View"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        '''GUI 초기화 메서드'''
        self.layout = QGridLayout()  # 레이아웃 설정
        self.layout.setContentsMargins(20, 20, 20, 20)  # 여백 추가

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
        self.toolbar.setStyleSheet(f'background-color: {Colors.baseColor01}; border-radius: 5px;')  # 배경색 및 테두리 설정
        self.toolbar.setFixedSize(300, 450)  # 크기 설정
        self.layout.addWidget(self.toolbar, 0, 0)

        # 상단 핵심 버튼 설정
        self.setup_core_buttons()

        # 중단 설정 (웹캠 선택, 비디오 배율)
        self.setup_video_options()

        # 하단 필터 리스트
        self.setup_filter_list()

    def setup_core_buttons(self):
        '''상단 핵심 버튼 설정 메서드'''
        font = QFont("Arial", 12)  # 폰트 설정

        # 실시간 영상 재생/중지 버튼
        self.play_pause_button = QPushButton("Play/Pause")
        self.play_pause_button.setFont(font)
        self.play_pause_button.clicked.connect(self.toggle_webcam)
        self.play_pause_button.setStyleSheet("QPushButton { border: 1px solid black; }")  # 윤곽선 추가

        # 일시정지 버튼
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFont(font)
        self.stop_button.clicked.connect(self.stop_webcam)
        self.stop_button.setStyleSheet("QPushButton { border: 1px solid black; }")  # 윤곽선 추가

        # 새 창 버튼
        self.new_window_button = QPushButton("New Window")
        self.new_window_button.setFont(font)
        self.new_window_button.clicked.connect(self.open_new_window)
        self.new_window_button.setStyleSheet("QPushButton { border: 1px solid black; }")  # 윤곽선 추가

        # 상단 버튼 레이아웃 설정
        core_buttons_layout = QHBoxLayout()
        core_buttons_layout.addWidget(self.play_pause_button)
        core_buttons_layout.addWidget(self.stop_button)
        core_buttons_layout.addWidget(self.new_window_button)
        core_buttons_layout.setSpacing(10)  # 버튼 사이 간격 설정

        self.toolbar.setLayout(core_buttons_layout)

    def setup_video_options(self):
        '''중단 비디오 옵션 설정 메서드'''
        font = QFont("Arial", 12)  # 폰트 설정

        # 웹캠 선택 콤보박스
        self.webcam_combo = QComboBox()
        self.webcam_combo.setFont(font)
        self.webcam_combo.addItems(["0", "1"])  # 임시 웹캠 목록
        self.webcam_combo.currentIndexChanged.connect(self.change_webcam)

        # 비디오 배율 콤보박스
        self.aspect_ratio_combo = QComboBox()
        self.aspect_ratio_combo.setFont(font)
        self.aspect_ratio_combo.addItems(["16:9", "3:4", "4:3", "9:16"])
        self.aspect_ratio_combo.currentIndexChanged.connect(self.change_aspect_ratio)

        # 중단 레이아웃 설정
        video_options_layout = QVBoxLayout()
        video_options_layout.addWidget(QLabel("Webcam:"))
        video_options_layout.addWidget(self.webcam_combo)
        video_options_layout.addWidget(QLabel("Aspect Ratio:"))
        video_options_layout.addWidget(self.aspect_ratio_combo)

        video_options_widget = QWidget()
        video_options_widget.setLayout(video_options_layout)

        self.layout.addWidget(video_options_widget, 0, 1)

    def setup_filter_list(self):
        '''하단 필터 리스트 설정 메서드'''
        font = QFont("Arial", 12)  # 폰트 설정

        # 필터 리스트
        self.filter_scroll_area = QScrollArea()
        self.filter_scroll_area.setWidgetResizable(True)
        self.filter_scroll_area.setFixedSize(300, 150)

        # 필터 버튼 생성
        self.flip_button = QPushButton("Flip Horizontal")
        self.flip_button.setFont(font)
        self.flip_button.clicked.connect(self.apply_flip)

        self.mosaic_button = QPushButton("Toggle Mosaic")
        self.mosaic_button.setFont(font)
        self.mosaic_button.clicked.connect(self.apply_mosaic)

        self.dummy_button = QPushButton("Dummy Button")
        self.dummy_button.setFont(font)
        self.dummy_button.clicked.connect(self.dummy_function)

        # 필터 버튼 레이아웃 설정
        filter_layout = QVBoxLayout()
        filter_layout.addWidget(self.flip_button)
        filter_layout.addWidget(self.mosaic_button)
        filter_layout.addWidget(self.dummy_button)
        filter_layout.setSpacing(10)

        filter_widget = QWidget()
        filter_widget.setLayout(filter_layout)

        self.filter_scroll_area.setWidget(filter_widget)

        self.layout.addWidget(self.filter_scroll_area, 1, 0, 1, 2)

    def setup_video_layer(self):
        '''비디오 레이어 설정 메서드'''
        self.video_widget = QLabel()  # 비디오 플레이어 레이블
        self.video_widget.setStyleSheet(f'background-color: {Colors.baseColor01}; border-radius: 10px;')  # 배경색 및 테두리 설정
        self.video_widget.setAlignment(Qt.AlignCenter)  # 정렬 설정
        self.layout.addWidget(self.video_widget, 0, 1)

    def setup_bottom_layer(self):
        '''하단 레이어 설정 메서드'''
        self.bottom_widget = QWidget()  # 하단 위젯
        self.bottom_widget.setStyleSheet(f'background-color: {Colors.baseColor01}; border-radius: 10px;')  # 배경색 및 테두리 설정
        self.bottom_layout = QVBoxLayout()  # 수직 레이아웃
        self.bottom_widget.setLayout(self.bottom_layout)

        self.layout.addWidget(self.bottom_widget, 1, 0, 1, 2)

    

    def toggle_webcam(self):
        '''웹캠 토글 메서드'''
        if self.play_pause_button.isChecked():
            if not self.video_processor.isRunning():
                self.video_processor.start()
                self.play_pause_button.setText("Stop Webcam")
                self.timer.start(0)  # 비동기적으로 프레임 업데이트
        else:
            if self.video_processor.isRunning():
                self.video_processor.stop()
                self.play_pause_button.setText("Start Webcam")
                self.timer.stop()

    def stop_webcam(self):
        '''웹캠 정지 메서드'''
        if self.video_processor.isRunning():
            self.video_processor.stop()
            self.play_pause_button.setText("Start Webcam")
            self.timer.stop()

    
    def open_new_window():
        '''새창 메서드'''
        # 웹캠 변경 로직 추가
        pass
    
    
    def change_webcam(self, index):
        '''웹캠 변경 메서드'''
        # 웹캠 변경 로직 추가
        pass



    def change_aspect_ratio(self, index):
        '''비디오 배율 변경 메서드'''
        # 비디오 배율 변경 로직 추가
        pass

    def apply_flip(self):
        '''좌우반전 필터 적용 메서드'''
        self.video_processor.flip_horizontal()
        # 좌우반전 필터 적용 로직 추가
        pass

    def apply_mosaic(self):
        '''모자이크 필터 적용 메서드'''
        if self.mosaic_button.isChecked():
            # 모자이크 활성화
            self.video_processor.mosaic_active = True
            self.mosaic_button.setText("Disable Mosaic")
        else:
            # 모자이크 비활성화
            self.video_processor.mosaic_active = False
            self.mosaic_button.setText("Toggle Mosaic")
        # 모자이크 필터 적용 로직 추가
        pass

    def dummy_function(self):
        '''더미 버튼 기능 메서드'''
        # 더미 버튼 기능 로직 추가
        pass

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

    
