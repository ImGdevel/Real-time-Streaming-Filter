from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QGridLayout, QVBoxLayout, QProgressDialog, QMessageBox
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from views.component import DragDropLabel, ImageItem, SettingWidget, FileViewWidget, FilterListWidget, ContentLabeling
from controllers import ImageProcessor
from utils import Colors, Style

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
        layout = QGridLayout()

        #dropbox 위젯
        self.dropbox_widget = DragDropLabel()
        self.dropbox_widget.drop_signal.connect(self.addItemFileView)

        #파일 뷰어 설정
        self.file_view_widget = FileViewWidget()
        self.file_view_widget.setMinimumSize(300, 200)
        self.file_view_widget.setMaximumHeight(300)
        
        self.file_view_widget.remove_file.connect(self.removeUrl)
        self.file_view_widget.add_file.connect(self.addItemFileView)
        self.file_view_widget.drop_signal.connect(self.addItemFileView)
        self.file_view_widget.image_change.connect(self.changeImage)

        setting_frame = QWidget()
        setting_frame.setMinimumWidth(200)
        setting_frame.setStyleSheet(Style.frame_style)
        setting_frame.setGraphicsEffect(Style.shadow(setting_frame))
        
        self.setting_widget = SettingWidget()


        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.onClickItemEvent.connect(self.set_filter_option)
        
        content_label = ContentLabeling()
        content_label.setLabel("필터 목록", Style.title_label)
        content_label.setContent(self.filter_list_widget)
        content_label.setContentMargin(0,0,0,0)
        
        self.setting_widget.addWidget(content_label)
        
        encoding_button = QPushButton("인코딩")
        encoding_button.setFixedHeight(40)
        encoding_button.setStyleSheet(Style.mini_button_style)
        encoding_button.clicked.connect(self.Encoding)

        download_button = QPushButton("다운로드")
        download_button.setFixedHeight(40)
        download_button.setStyleSheet(Style.mini_button_style)
        download_button.clicked.connect(self.Download)
        
        setting_layout = QVBoxLayout()
        setting_layout.setContentsMargins(0,5,0,10)
        setting_layout.addWidget(self.setting_widget)
        setting_button_layout = QVBoxLayout()
        setting_button_frame = QWidget()
        setting_button_layout.setContentsMargins(15,0,15,5)
        setting_button_layout.addWidget(encoding_button)
        setting_button_layout.addWidget(download_button)
        setting_button_frame.setLayout(setting_button_layout)
        setting_layout.addWidget(setting_button_frame)
        setting_frame.setLayout(setting_layout)
        
        layout.addWidget(self.dropbox_widget, 0, 0)
        layout.addWidget(setting_frame, 0, 1)
        layout.addWidget(self.file_view_widget, 1, 0, 1, 2)

        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 1)
        
        layout.setColumnStretch(0, 5)
        layout.setColumnStretch(1, 1)

        self.setLayout(layout)

    
    def removeUrl(self, url):
        i = int()
        if url.toLocalFile() == self.dropbox_widget.currunt_exm:
            i = self.urls.index(url)
            if i+1 == len(self.urls):
                i = i-1

        self.urls.remove(url)
        if self.filtered_image:
            del self.filtered_image[url.toLocalFile()]

        if url.toLocalFile() == self.dropbox_widget.currunt_exm and len(self.urls) != 0:
            self.dropbox_widget.currunt_exm = self.urls[i].toLocalFile()
            if self.filtered_image:
                self.dropbox_widget.currunt_filt = self.filtered_image[self.urls[i].toLocalFile()]
            self.dropbox_widget.refreashWidget()
        elif not self.urls:
            self.dropbox_widget.emptyExmLabel()
            self.dropbox_widget.currunt_exm = None
            self.dropbox_widget.emptyFiletLabel()
            self.dropbox_widget.currunt_filt = None


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
            self.dropbox_widget.currunt_exm = file_path
            if self.dropbox_widget.currunt_filt != None:
                self.dropbox_widget.currunt_filt = None
                self.dropbox_widget.emptyFiletLabel()
            self.file_view_widget.addNewFile(add_urls)

    def changeImage(self, url):
        file_path = url.toLocalFile()
        self.dropbox_widget.setExampleView(file_path)
        self.dropbox_widget.currunt_exm = file_path
        if self.filtered_image.get(url.toLocalFile()) != None:
            print("in")
            self.dropbox_widget.setFilteredView(self.filtered_image.get(url.toLocalFile()))
            self.dropbox_widget.currunt_filt = self.filtered_image.get(url.toLocalFile())
        else :
            self.dropbox_widget.currunt_filt = None
            self.dropbox_widget.emptyFiletLabel()

    def Encoding(self):
        url_list = self.UrlListConverter(self.urls)
        if url_list:
            progress_dialog = QProgressDialog("Encoding", "Cancel", 0, 100)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()
            self.filtered_image = self.filter_image_processor.filtering_images_to_dict(url_list, progress_dialog)
            print(self.filtered_image)
            self.changeImage(QUrl.fromLocalFile(self.dropbox_widget.currunt_exm))
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("인코딩이 완료되었습니다")
            msg.setWindowTitle("알림")
            msg.exec_()
            
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("등록된 이미지가 존재하지 않습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()
    
    def Download(self):
        if self.filtered_image:
            self.filter_image_processor.create_filtered_image_dict(self.filtered_image)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("다운로드가 완료되었습니다")
            msg.setWindowTitle("알림")
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("인코딩된 이미지가 존재하지 않습니다")
            msg.setWindowTitle("경고")
            msg.exec_()


    def UrlListConverter(self, urls):
        origin_urls =list()
        if urls:
            for url in urls:
                origin_urls.append(url.toLocalFile())
        
        return origin_urls
        
    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_list()
        pass

    def swap_event(self):
        
        pass