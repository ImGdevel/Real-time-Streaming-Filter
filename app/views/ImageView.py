from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QGridLayout, QVBoxLayout, QProgressDialog
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from .component import DragDropLabel, ImageItem, SettingWidget, FileViewWidget, FilterListWidget
from controllers import ImageProcessor
from utils import Colors

class ImageView(QWidget):
    
    count = int
    urls = list()
    filtered_image = dict()

    def __init__(self, parent = None):

        super().__init__(parent)

        self.filter_image_processor = ImageProcessor()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.count = 0
        # 전체 레이아웃 설정
        self.layout = QVBoxLayout()

        self.top_widget = QWidget()
        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(1)

        #dropbox 위젯
        self.dropbox_widget = DragDropLabel()
        self.dropbox_widget.drop_signal.connect(self.addItemFileView)

        #파일 뷰어 설정
        self.file_view_widget = FileViewWidget()
        self.file_view_widget.setMinimumSize(300, 150)
        self.file_view_widget.setMaximumHeight(250)
        
        self.file_view_widget.remove_file.connect(self.removeUrl)
        self.file_view_widget.add_file.connect(self.addItemFileView)
        self.file_view_widget.drop_signal.connect(self.addItemFileView)
        self.file_view_widget.image_change.connect(self.changeImage)

        self.setting_frame = QWidget()
        self.setting_widget = SettingWidget()
        self.setting_widget.Encoding_button.clicked.connect(self.Encoding)

        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.onClickItemEvent.connect(self.set_filter_option)
        self.filter_list_widget.setMinimumHeight(275)
        self.setting_widget.addWidget(self.filter_list_widget)

        self.download_button = QPushButton("Download")
        self.download_button.setFixedHeight(50)
        self.download_button.clicked.connect(self.Download)
        self.setting_widget.addWidget(self.download_button)
        
        self.setting_frame.setMinimumSize(100, 150)
        self.setting_frame.setMaximumWidth(235)
        self.setting_layout = QVBoxLayout()
        self.setting_layout.addWidget(self.setting_widget)
        self.setting_frame.setLayout(self.setting_layout)

        self.top_layout.addWidget(self.dropbox_widget)
        self.top_layout.addWidget(self.setting_frame)
        self.top_widget.setLayout(self.top_layout)
        self.layout.addWidget(self.top_widget)
        self.layout.addWidget(self.file_view_widget)

        self.setLayout(self.layout)

    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_list()
        pass
    
    def removeUrl(self, url):
        self.urls.remove(url)
        if self.filtered_image:
            del self.filtered_image[url.toLocalFile()]

    def set_filter_option(self, index):
        """필터 옵션 선택"""
        self.filter_image_processor.set_filter(index)
        pass

    def addItemFileView(self, urls):
        add_urls = list()
        for i in urls:
            if i not in self.urls:
                self.urls.append(i) 
                add_urls.append(i)
        
        if add_urls :
            file_path = add_urls[0].toLocalFile()
            self.dropbox_widget.setExampleView(file_path)
            self.file_view_widget.addNewFile(add_urls)

    def changeImage(self, url):
        file_path = url.toLocalFile()
        self.dropbox_widget.setExampleView(file_path)
        if self.filtered_image:
            print("in")
            self.dropbox_widget.setFilteredView(self.filtered_image.get(url.toLocalFile()))

    def Encoding(self):
        url_list = self.UrlListConverter(self.urls)
        if url_list:
            progress_dialog = QProgressDialog("Encoding", "Cancel", 0, 100)
            progress_dialog.setWindowModality(Qt.WindowModal)
            # progress_dialog.setStyleSheet('''
            #     background-color: #333333; /* Dark gray background */
            #     color: #FFFFFF; /* White text */
            #     font-size: 16px; /* Font size */
            #     padding: 20px; /* Padding */
            # ''')
            progress_dialog.show()
            self.filtered_image = self.filter_image_processor.filtering_images_to_dict(url_list, progress_dialog)
            #print(self.filtered_image)
    
    def Download(self):
        if self.filtered_image:
            self.filter_image_processor.create_filtered_image_dict(self.filtered_image)

    def UrlListConverter(self, urls):
        origin_urls =list()
        if urls:
            for url in urls:
                origin_urls.append(url.toLocalFile())
        
        return origin_urls
        

   