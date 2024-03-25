from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from .title_bar import MyTitleBar

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
        self.tool_widget.setStyleSheet("background-color: #333333;")  # 더 진한 배경색으로 변경
        self.tool_widget.setMinimumSize(1000, 120)  # 최소 크기 설정
        self.grid_layout.addWidget(self.tool_widget, 1, 0, 1, 3)  # 상단 도구 영역

        # 기능 메뉴 영역
        self.menu_widget = QWidget()
        self.menu_widget.setStyleSheet("background-color: #444444;")  # 더 진한 배경색으로 변경
        self.menu_widget.setMinimumSize(300, 500)  # 최소 크기 설정
        self.grid_layout.addWidget(self.menu_widget, 2, 0)  # 기능 메뉴 영역

        # 기능 설명 및 기능들 영역
        self.description_widget = QWidget()
        self.description_widget.setStyleSheet("background-color: #555555;")  # 더 진한 배경색으로 변경
        self.description_widget.setMinimumSize(700, 500)  # 최소 크기 설정
        self.grid_layout.addWidget(self.description_widget, 2, 1, 1, 2)  # 기능 설명 및 기능들 영역


        # 그리드 레이아웃을 전체 레이아웃에 추가
        self.layout.addLayout(self.grid_layout)

        self.layout.setContentsMargins(0, 0, 0, 0)  # 창과의 간격 설정
        self.layout.addStretch(-1)

        self.setLayout(self.layout)

        # 전체 애플리케이션의 스타일 설정
        self.setStyleSheet("""
            background-color: #212121;
            color: #ffffff;
            font-family: Arial, sans-serif;
        """)
        
        # 프레임리스 윈도우 설정
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

    def center(self):
        """윈도우를 화면 중앙으로 위치시키는 메서드"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
