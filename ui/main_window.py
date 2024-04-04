from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from ui.title_bar import MyTitleBar
from ui.colors import Colors
from ui.menu import Menu
from ui.router import Router

# ********* 페이지(레이어)는 router.py에서 등록 **********

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
        self.layout.addWidget(MyTitleBar(self))
        self.layout.setSpacing(10)  # 간격 설정

        # 전체 레이아웃 설정
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 10)  # 상단, 하단, 좌측, 우측 여백 설정

        # 오른쪽 1/4 공간 - 메뉴바
        self.right_widget = QWidget()
        self.right_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.right_widget.setFixedWidth(200)

        # Menu 위젯 추가
        self.menu = Menu()
        self.menu_layout = QVBoxLayout()
        self.menu_layout.addWidget(self.menu)
        self.right_widget.setLayout(self.menu_layout)

        # 나머지 구간 - 컨텐츠
        self.remaining_widget = QWidget()
        self.remaining_widget.setStyleSheet(f'background-color: {Colors.baseColor02};')
        self.remaining_widget.setMinimumWidth(500)

        # QHBoxLayout 추가
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.right_widget)
        self.hbox_layout.addWidget(self.remaining_widget)

        # QStackedWidget 추가
        self.contentLayout = QStackedWidget()

        # Router 생성 및 전달
        self.router = Router(self.contentLayout, self.menu)

        self.remaining_layout = QVBoxLayout()
        self.remaining_layout.addWidget(self.contentLayout)
        self.remaining_widget.setLayout(self.remaining_layout)

        self.main_layout.addLayout(self.hbox_layout)
        self.layout.addLayout(self.main_layout)

        self.layout.setContentsMargins(0, 0, 0, 0)  # 모든 여백 제거
        self.setLayout(self.layout)

        self.setStyleSheet(f"""
            background-color: {Colors.baseColor01};
            color: {Colors.textColor01};
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
