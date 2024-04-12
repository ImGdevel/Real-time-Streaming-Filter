from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QGridLayout, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from utils.colors import Colors
from .image_item import ImageItem

class FileViewWidget(QWidget):
    count = int
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.remove_mode = False
        self.count = 0
        self.layout = QVBoxLayout()

        #file view
        self.file_box_layout = QHBoxLayout()
        self.file_view_widget = QWidget()
        self.file_view_widget.setMinimumSize(500, 250)
        self.file_view_widget.setMaximumWidth(500)
        self.file_view_widget.setMaximumHeight(250)
        self.file_view_widget.setLayout(self.file_box_layout)
        self.file_view_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(False)
        scroll_area.setWidget(self.file_view_widget)

        #button
        self.button_widget = QWidget()
        self.button_widget.setFixedSize(300, 50)
        self.button_layout = QHBoxLayout()

        self.remove_button = QPushButton("Del")
        self.remove_button.clicked.connect(self.setRemoveMode)
        
        self.file_explorer_button = QPushButton("Serch")
        self.file_explorer_button.clicked.connect(self.openFileExplorer)
        
        self.button_layout.addWidget(self.remove_button)
        self.button_layout.addWidget(self.file_explorer_button)
        self.button_widget.setLayout(self.button_layout)

        #set frame layout
        self.layout.addWidget(self.file_view_widget)
        self.layout.addWidget(self.button_widget)
        self.setLayout(self.layout)
        

    def setRemoveMode(self):
        if self.remove_mode:
            print("off")
            self.remove_mode = False
        else :
            self.remove_mode = True
            print("on")

    def openFileExplorer(self):
        print("FileExplorer")

    def addNewFile(self, urls):
        for i, file_info in enumerate(urls):
            file_widget = ImageItem(file_info)
            file_widget.delet_signal.connect(self.removeFile)
            self.file_box_layout.addWidget(file_widget)
            self.count += 1

    def removeFile(self, widget):
        if self.remove_mode:
            self.file_box_layout.removeWidget(widget)
            widget.deleteLater()


