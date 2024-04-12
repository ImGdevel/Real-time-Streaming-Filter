from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from utils.colors import Colors
from .component import DragDropLabel, ImageItem, SettingWidget, FileViewWidget

class ImageView(QWidget):

    count = int

    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.count = 0
        # 전체 레이아웃 설정
        self.layout = QGridLayout()
        #dropbox 위젯
        self.dropbox_widget = DragDropLabel()
        self.dropbox_widget.drop_signal.connect(self.addItemFileView)

        #파일 뷰어 설정
        self.file_view_widget = FileViewWidget()
        self.file_view_widget.setMinimumSize(300, 150)
        self.file_view_widget.setMaximumWidth(500)
        self.file_view_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        
        self.setting_frame = QWidget()
        self.setting_widget = SettingWidget()
        self.setting_frame.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.setting_frame.setMinimumSize(100, 150)
        self.setting_frame.setMaximumWidth(200)
        self.setting_layout = QVBoxLayout()
        self.setting_layout.addWidget(self.setting_widget)
        self.setting_frame.setLayout(self.setting_layout)

        self.layout.addWidget(self.dropbox_widget, 0, 0,)
        self.layout.addWidget(self.setting_frame, 0, 1)
        self.layout.addWidget(self.file_view_widget, 1, 0)

        self.setLayout(self.layout)
    


    def addItemFileView(self, urls):
        self.file_view_widget.addNewFile(urls)




   