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

        # page button 추가
        self.addMenuButton("Home", 0)
        self.addMenuButton("Stream",1)
        self.addMenuButton("Video", 2)
        self.addMenuButton("Image",3)
        self.addMenuButton("Setting",4)

        # 상단에 여백 추가
        self.layout.addStretch()

        self.setLayout(self.layout)

    def addMenuButton(self, name, number):
        self.button = QPushButton(name)
        self.button.clicked.connect(lambda: self.page_changed.emit(number)) 
        self.layout.addWidget(self.button)
