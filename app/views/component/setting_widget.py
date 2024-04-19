from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget
from PyQt5.QtGui import QImage, QPixmap
from utils import Colors



class SettingWidget(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.download_button = QPushButton("Download")
        
        self.layout.addWidget(self.download_button)
        self.setLayout(self.layout)

    def addSettingButton(self, button):
        self.layout.addWidget(button)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
