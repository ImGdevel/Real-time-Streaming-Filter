from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from utils.colors import Colors
from .component import DragDropLabel, ImageItem, SettingWidget 

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
        self.file_grid_layout = QGridLayout()
        self.file_view_widget = QWidget()
        self.file_view_widget.setLayout(self.file_grid_layout)
        self.file_view_widget.setMinimumSize(300, 150)
        self.file_view_widget.setMaximumWidth(500)
        self.file_view_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        

        self.setting_widget = SettingWidget()
        self.setting_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.setting_widget.setMinimumSize(100, 150)
        self.setting_widget.setMaximumWidth(200)

        self.layout.addWidget(self.dropbox_widget, 0, 0,)
        self.layout.addWidget(self.setting_widget, 0, 1)
        self.layout.addWidget(self.file_view_widget, 1, 0)

        self.setLayout(self.layout)
    


    def addItemFileView(self, urls):
        num_cols = 7  # Number of columns in the grid
        # Populate the grid layout with file widgets
        row = self.count//num_cols
        col = self.count % num_cols
        print(self.count)
        for i, file_info in enumerate(urls):
            print(self.count)
            if col == num_cols:
                row += 1
                col = 0
            print(row,", ", col)
            file_widget = ImageItem(file_info)
            self.file_view_widget.layout().addWidget(file_widget, row, col)
            self.count += 1
            col += 1



   