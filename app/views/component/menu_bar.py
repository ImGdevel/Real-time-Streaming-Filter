from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class MenuBar(QWidget):

    # 페이지 변경 시그널 정의
    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()  # 수직 레이아웃 사용

        self.button1 = QPushButton("Home")
        self.button1.clicked.connect(lambda: self.page_changed.emit(0)) 
        self.layout.addWidget(self.button1)

        self.button2 = QPushButton("Page1")
        self.button2.clicked.connect(lambda: self.page_changed.emit(1)) 
        self.layout.addWidget(self.button2)

        # 상단에 여백 추가
        self.layout.addStretch()

        self.setLayout(self.layout)
