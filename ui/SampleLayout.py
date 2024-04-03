from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from .colors import Colors
<<<<<<<< HEAD:ui/HomePage.py
from .SampleLayout import SampleLayout

class HomePage(QWidget):
    def __init__(self, parent=None):
========

class SampleLayout(QWidget):
    def __init__(self, parent = None):
>>>>>>>> 390ef1365d90bbf66441477f75d9d0b028ffa276:ui/SampleLayout.py
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QGridLayout()

        # 오른쪽 1/4 공간 - 메뉴바
<<<<<<<< HEAD:ui/HomePage.py
        self.right_widget = QWidget()
        self.right_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.right_widget.setMinimumSize(150, 700)
        self.layout.addWidget(self.right_widget, 0, 0, 1, 1)

        # 나머지 구간 - 컨텐츠
        self.remaining_widget = QWidget()
        self.remaining_widget.setStyleSheet(f'background-color: {Colors.baseColor02};')
        self.remaining_widget.setFixedWidth(768)
        self.layout.addWidget(self.remaining_widget, 0, 1, 1, 1)

        # QStackedWidget 추가
        self.contentLayout = QStackedWidget()

        self.sampleLayout = SampleLayout()
        self.contentLayout.addWidget(self.sampleLayout)

        self.remaining_layout = QVBoxLayout()
        self.remaining_layout.addWidget(self.contentLayout)
        self.remaining_widget.setLayout(self.remaining_layout)

        self.setLayout(self.layout)
========
        right_widget = QWidget()
        right_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        right_widget.setMinimumSize(100, 700)
        layout.addWidget(right_widget, 0, 0, 1, 1)

        # 나머지 구간 - 컨텐츠
        remaining_widget = QWidget()
        remaining_widget.setStyleSheet(f'background-color: {Colors.baseColor02};')
        remaining_widget.setMinimumSize(500, 700)
        layout.addWidget(remaining_widget, 0, 1, 1, 1)


        self.setLayout(layout)
>>>>>>>> 390ef1365d90bbf66441477f75d9d0b028ffa276:ui/SampleLayout.py
