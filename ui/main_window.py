from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from .title_bar import MyTitleBar
from .video_processor import VideoProcessor
from .colors import Colors

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        # 윈도우 설정
        self.setWindowTitle('Real-time video filtering program')
        self.setFixedSize(1024, 768)
        self.center()

        # 레이아웃 및 타이틀 바 추가
        self.layout = QVBoxLayout()
        
        # 타이틀 바 추가
        self.layout.addWidget(MyTitleBar(self))
        
        # 그리드 레이아웃 추가
        self.grid_layout = QGridLayout()

        # 상단 도구 영역
        self.tool_widget = QWidget()
        self.tool_widget.setStyleSheet(f"background-color: {Colors.btnColor02};")  # 더 진한 배경색으로 변경
        self.tool_widget.setMinimumSize(1000, 120)  # 최소 크기 설정
        self.grid_layout.addWidget(self.tool_widget, 1, 0, 1, 3)  # 상단 도구 영역

        # 기능 메뉴 영역
        self.menu_widget = QWidget()
        self.menu_widget.setStyleSheet(f"background-color: {Colors.btnColor02};")  # 더 진한 배경색으로 변경
        self.menu_widget.setMinimumSize(300, 500)  # 최소 크기 설정
        self.grid_layout.addWidget(self.menu_widget, 2, 0)  # 기능 메뉴 영역

        # 기능 설명 및 기능들 영역
        self.description_widget = QWidget()
        self.description_widget.setStyleSheet(f"background-color: {Colors.btnColor02};")  # 더 진한 배경색으로 변경
        self.description_widget.setMinimumSize(700, 500)  # 최소 크기 설정
        self.grid_layout.addWidget(self.description_widget, 2, 1, 1, 2)  # 기능 설명 및 기능들 영역


        # 그리드 레이아웃을 전체 레이아웃에 추가
        self.layout.addLayout(self.grid_layout)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 창과의 간격 설정
        self.layout.addStretch(-1)
        self.setLayout(self.layout)


        # 수직 박스 레이아웃 생성 (버튼을 수직으로 배치하기 위해)
        self.button_layout = QVBoxLayout()

        self.gray_button = QPushButton("Grayscale Mode (OFF)")
        self.gray_button.setCheckable(True)
        self.gray_button.clicked.connect(self.toggle_gray_mode)
        self.button_layout.addWidget(self.gray_button)

        self.invert_button = QPushButton("Invert Mode (OFF)")
        self.invert_button.setCheckable(True)
        self.invert_button.clicked.connect(self.toggle_invert_mode)
        self.button_layout.addWidget(self.invert_button)

        self.mosaic_button = QPushButton("Mosaic Mode (OFF)")
        self.mosaic_button.setCheckable(True)
        self.mosaic_button.clicked.connect(self.toggle_mosaic_mode)
        self.button_layout.addWidget(self.mosaic_button)

        # 빈 QLabel을 추가하여 버튼들이 아래쪽으로 정렬되도록 함
        self.button_layout.addWidget(QLabel())

        # 기능 메뉴 영역의 레이아웃을 버튼 레이아웃으로 설정
        self.menu_widget.setLayout(self.button_layout)


        # 수직 박스 레이아웃 생성 (영상을 수직으로 배치하기 위해)
        self.video_layout = QVBoxLayout()

        self.video_label1 = QLabel()
        self.video_label2 = QLabel()

        self.video_layout.addWidget(self.video_label1)
        self.video_layout.addWidget(self.video_label2)

        self.description_widget.setLayout(self.video_layout)

        self.video_processor = VideoProcessor()  # VideoProcessor 객체 생성

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.gray_mode = False
        self.invert_mode = False
        self.mosaic_mode = False

        self.setStyleSheet(f"""
            background-color: {Colors.baseColor01};
            color: {Colors.textColor01};
            font-family: Arial, sans-serif;
        """)
        
        # 프레임리스 윈도우 설정
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

    def toggle_gray_mode(self, checked):
        self.gray_mode = checked
        if self.gray_mode:
            self.gray_button.setText("Grayscale Mode (ON)")
        else:
            self.gray_button.setText("Grayscale Mode (OFF)")
        self.update_frame()

    def toggle_invert_mode(self, checked):
        self.invert_mode = checked
        if self.invert_mode:
            self.invert_button.setText("Invert Mode (ON)")
        else:
            self.invert_button.setText("Invert Mode (OFF)")
        self.update_frame()

    def toggle_mosaic_mode(self, checked):
        self.mosaic_mode = checked
        if self.mosaic_mode:
            self.mosaic_button.setText("Mosaic Mode (ON)")
        else:
            self.mosaic_button.setText("Mosaic Mode (OFF)")
        self.update_frame()

    def update_frame(self):
        frame = self.video_processor.get_frame()

        if frame is not None:
            # 원본 영상
            q_img1 = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap1 = QPixmap.fromImage(q_img1).scaled(320, 240, aspectRatioMode=Qt.KeepAspectRatio)
            self.video_label1.setPixmap(pixmap1)

            # 영상 처리
            if self.gray_mode:
                processed_frame = self.video_processor.convert_to_grayscale(frame)
            elif self.invert_mode:
                processed_frame = self.video_processor.invert_colors(frame)
            elif self.mosaic_mode:
                processed_frame = self.video_processor.mosaic_face(frame.copy())  # 원본 프레임의 복사본을 사용
            else:
                processed_frame = frame
            
            q_img2 = QImage(processed_frame.data, processed_frame.shape[1], processed_frame.shape[0], QImage.Format_RGB888)
            pixmap2 = QPixmap.fromImage(q_img2).scaled(320, 240, aspectRatioMode=Qt.KeepAspectRatio)
            self.video_label2.setPixmap(pixmap2)



    def center(self):
        """윈도우를 화면 중앙으로 위치시키는 메서드"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
