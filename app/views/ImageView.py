from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from utils import Colors

class ImageView(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QGridLayout()


        self.setLayout(self.layout)
