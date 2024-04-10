from PyQt5.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from utils import Colors

class RStreamPage(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.grid_layout = QGridLayout()
        self.hbox_layout = QHBoxLayout()
        #1열 위젯설정
        self.top_widget = QWidget()

        self.left_widget = QWidget()
        self.left_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.left_widget.setMaximumWidth(200)
        self.hbox_layout.addWidget(self.left_widget)

        self.remaining_widget = QWidget()
        self.remaining_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.remaining_widget.setFixedWidth(618)
        self.hbox_layout.addWidget(self.remaining_widget)
        
        self.top_widget.setLayout(self.hbox_layout)
        self.grid_layout.addWidget(self.top_widget, 0, 0, 1, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.bottom_widget.setFixedWidth(768)
        self.grid_layout.addWidget(self.bottom_widget, 1, 0, 1, 1)


        self.setLayout(self.grid_layout)
