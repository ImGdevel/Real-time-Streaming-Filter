from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from utils.colors import Colors
from .component import DragDropLabel, ImageItem, SettingWidget 

class ImageView(QWidget):

    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        # 전체 레이아웃 설정
        self.layout = QGridLayout()
        #dropbox 위젯
        self.dropbox_widget = DragDropLabel()
        self.dropbox_widget.drop_signal.connect(self.addItemFileView)

        #파일 뷰어 설정
        self.file_grid_layout = QGridLayout()
        self.file_grid_layout.setAlignment(Qt.AlignLeft)
        self.file_view_widget = QWidget()
        self.file_view_widget.setLayout(self.file_grid_layout)
        self.file_view_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        

        self.setting_widget = SettingWidget()

        self.layout.addWidget(self.dropbox_widget, 0, 0, 1, 1)
        self.layout.addWidget(self.setting_widget, 0, 1, 1, 1)
        self.layout.addWidget(self.file_view_widget, 1, 0, 1, 1)

        self.setLayout(self.layout)
    


    def addItemFileView(self, urls):
        num_cols = 7  # Number of columns in the grid

        # Populate the grid layout with file widgets
        for i, file_info in enumerate(urls):
            row = i // num_cols
            col = i % num_cols
            file_widget = ImageItem(file_info)
            self.file_view_widget.layout().addWidget(file_widget, row, col)



   