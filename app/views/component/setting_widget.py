from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget
from PySide6.QtGui import QImage, QPixmap
from utils import Colors, Style

class SettingWidget(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(Style.frame_style)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(3)
        self.setLayout(self.layout)

    def addSettingButton(self, button):
        self.layout.addWidget(button)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
