from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from .colors import Colors

class SampleLayout(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 레이아웃 설정
        layout = QGridLayout()

        # 오른쪽 1/4 공간 - 메뉴바
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
