from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class MenuBar(QWidget):

    # 페이지 변경 시그널 정의
    page_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()  # 수직 레이아웃 사용
        self.setContentsMargins(0,10,0,10)
        # page button 추가
        self.addMenuButton("Home", 0)
        self.addMenuButton("Stream", 1)
        self.addMenuButton("Video", 2)
        self.addMenuButton("Image", 3)
        self.addMenuButton("Filter", 4)
        self.addMenuButton("Setting", 5)

        # 상단에 여백 추가
        self.layout.addStretch()

        self.setLayout(self.layout)

    def addMenuButton(self, name, number):
        self.button = QPushButton(name)
        self.button.setFixedSize(150, 50)
        self.button.clicked.connect(lambda: self.page_changed.emit(number)) 
        self.layout.addWidget(self.button)
