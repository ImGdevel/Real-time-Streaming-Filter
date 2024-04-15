from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from utils.colors import Colors
from .component import DragDropLabel, ImageItem, SettingWidget, FileViewWidget

class ImageView(QWidget):

    count = int
    urls = list()

    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.count = 0
        # 전체 레이아웃 설정
        self.layout = QVBoxLayout()

        self.top_widget = QWidget()
        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(7)

        #dropbox 위젯
        self.dropbox_widget = DragDropLabel()
        self.dropbox_widget.drop_signal.connect(self.addItemFileView)

        #파일 뷰어 설정
        self.file_view_widget = FileViewWidget()
        self.file_view_widget.setMinimumSize(300, 150)
        self.file_view_widget.setMaximumWidth(800)
        self.file_view_widget.setMaximumHeight(350)
        self.file_view_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.file_view_widget.remove_file.connect(self.removeUrl)
        self.file_view_widget.add_file.connect(self.addItemFileView)
        
        self.setting_frame = QWidget()
        self.setting_widget = SettingWidget()
        self.setting_widget.download_button.clicked.connect(self.Download)
        self.setting_frame.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.setting_frame.setMinimumSize(100, 150)
        self.setting_frame.setMaximumWidth(200)
        self.setting_layout = QVBoxLayout()
        self.setting_layout.addWidget(self.setting_widget)
        self.setting_frame.setLayout(self.setting_layout)

        self.top_layout.addWidget(self.dropbox_widget)
        self.top_layout.addWidget(self.setting_frame)
        self.top_widget.setLayout(self.top_layout)
        self.layout.addWidget(self.top_widget)
        self.layout.addWidget(self.file_view_widget)

        self.setLayout(self.layout)
    
    def removeUrl(self, url):
        self.urls.remove(url)

    def addItemFileView(self, urls):
        add_urls = list()
        for i in urls:
            if i not in self.urls:
                self.urls.append(i) 
                add_urls.append(i)
        file_path = add_urls[0].toLocalFile()
        self.dropbox_widget.setExampleView(file_path)
        self.file_view_widget.addNewFile(add_urls)

    def Download(self):
        print("download")




   