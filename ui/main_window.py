from PyQt5.QtWidgets import QDesktopWidget, QVBoxLayout, QWidget, QGridLayout, QStackedWidget
from PyQt5.QtCore import  Qt
from .title_bar import MyTitleBar
from .colors import Colors
from .page1 import Page1
from .page2 import Page2
from .HomePage import HomePage

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
        
        # QStackedWidget 추가
        self.stacked_widget = QStackedWidget()
        
        # 페이지 생성 및 QStackedWidget에 추가
        #self.page1 = Page1()
        #self.stacked_widget.addWidget(self.page1)
        #self.page2 = Page2()
        #self.stacked_widget.addWidget(self.page2)
        self.homepage = HomePage()
        self.stacked_widget.addWidget(self.homepage)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.stacked_widget, 0, 0, 1, 3)

        # 그리드 레이아웃을 전체 레이아웃에 추가
        self.layout.addLayout(self.grid_layout)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 창과의 간격 설정
        self.layout.addStretch(-1)
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
