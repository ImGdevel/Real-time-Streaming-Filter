from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget
from PyQt5.QtGui import QImage, QPixmap
from utils import Colors



class SettingWidget(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.setMinimumSize(100, 300)
        self.download_button = QPushButton()
        self.setLayout(self.layout)
        

