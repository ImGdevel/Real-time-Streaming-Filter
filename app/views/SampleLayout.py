from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from utils import Colors

class SampleLayout(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QGridLayout()

        # 오른쪽 1/4 공간 - 메뉴바

        self.right_widget = QWidget()
        self.right_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.right_widget.setMinimumSize(150, 700)
        self.layout.addWidget(self.right_widget, 0, 0, 1, 1)

        # 나머지 구간 - 컨텐츠
        self.remaining_widget = QWidget()
        self.remaining_widget.setStyleSheet(f'background-color: {Colors.baseColor02};')
        self.remaining_widget.setFixedWidth(768)
        self.layout.addWidget(self.remaining_widget, 0, 1, 1, 1)


        self.setLayout(self.layout)
