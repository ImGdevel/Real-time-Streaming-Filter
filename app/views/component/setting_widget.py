from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget
from PySide6.QtGui import QImage, QPixmap


class SettingWidget(QWidget):
    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.Encoding_button = QPushButton("Encoding")
        self.Encoding_button.setMaximumHeight(50)

        self.layout.addWidget(self.Encoding_button)
        self.setLayout(self.layout)

    def addSettingButton(self, button):
        self.layout.addWidget(button)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
