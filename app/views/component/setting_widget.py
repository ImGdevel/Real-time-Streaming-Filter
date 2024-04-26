from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget
from PySide6.QtGui import QImage, QPixmap


class SettingWidget(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.incoding_button = QPushButton("Incoding")
        
        self.layout.addWidget(self.incoding_button)
        self.setLayout(self.layout)

    def addSettingButton(self, button):
        self.layout.addWidget(button)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
