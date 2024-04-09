from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QMimeDatabase
from utils import Colors
from component.drag_drop import DragDropLabel
from component.image_item import ImageItem

class ImageView(QWidget):

    def __init__(self, parent = None):

        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QGridLayout()
        
        #dropbox 위젯
        self.dropbox_widget = DragDropLabel()

        #파일 뷰어 설정
        self.file_grid_layout = QGridLayout()
        self.file_view_widget = QWidget()
        self.file_view_widget.setLayout(self.file_grid_layout)


        self.setting_widget = QWidget()

        self.layout.addWidget(self.dropbox_widget, 0, 0, 1, 1)
        self.setLayout(self.layout)


    def addItemFileView(self):
        files = self.dropbox_widget.getUrls()
        num_cols = 3  # Number of columns in the grid

        # Populate the grid layout with file widgets
        for i, file_info in enumerate(files):
            row = i // num_cols
            col = i % num_cols

            file_widget = ImageItem(file_info)
            self.file_grid_layout.addWidget(file_widget, row, col)



   