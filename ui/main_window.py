from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from .title_bar import MyTitleBar

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """전체 애플리케이션 UI 초기화 메서드"""
        # 윈도우 설정
        self.setWindowTitle('Real-time video filtering program')
        self.setFixedSize(1024, 768)
        self.center()

        # 레이아웃 및 타이틀 바 추가
        self.layout = QVBoxLayout()
        self.layout.addWidget(MyTitleBar(self))
        self.layout.setContentsMargins(0, 0, 0, 0)
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
