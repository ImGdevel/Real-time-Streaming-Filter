from utils.colors import Colors
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QVBoxLayout, QScrollArea, QLabel, QBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QUrl, Signal, QMimeDatabase
from PySide6.QtGui import QDragEnterEvent, QIcon, QDesktopServices
from .image_item import ImageItem
import os
from urllib.parse import urlparse
from utils import Style, Icons

class FileViewWidget(QWidget):
    drop_signal = Signal(list)
    count = int
    remove_file = Signal(QUrl)
    image_change = Signal(QUrl)
    add_file = Signal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.remove_mode = False
        self.count = 0
        self.layout = QHBoxLayout()
        #file view
        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.file_view_label = QLabel()
        self.scroll_widget = QWidget()
        self.file_view_label.setContentsMargins(0,0,0,0)
        self.file_box_layout = QHBoxLayout()
        self.scroll_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.file_box_layout.addWidget(self.scroll_area)
        self.file_view_label.setLayout(self.file_box_layout)
        self.file_view_label.setAcceptDrops(True)
        self.file_view_label.dragEnterEvent = self.dragEnterEvent
        self.file_view_label.dropEvent = self.dropEvent
        self.scroll_layout.addStretch()
        self.scroll_layout.setDirection(QBoxLayout.RightToLeft)
        #button
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout()

        self.remove_button = QPushButton()
        self.remove_button.setToolTip("파일삭제")
        self.remove_button.setFixedSize(50, 50)
        self.remove_button.setIcon(QIcon(Icons.dust_bin))
        self.remove_button.clicked.connect(self.setRemoveMode)
        
        self.file_explorer_button = QPushButton()
        self.file_explorer_button.setToolTip('파일탐색')
        self.file_explorer_button.setFixedSize(50, 50)
        self.file_explorer_button.setIcon(QIcon(Icons.folder_open))
        self.file_explorer_button.clicked.connect(self.openFileExplorer)
        
        self.button_layout.addWidget(self.file_explorer_button)
        self.button_layout.addWidget(self.remove_button)
        self.button_widget.setLayout(self.button_layout)

        #set frame layout
        self.layout.addWidget(self.button_widget)
        self.layout.addWidget(self.file_view_label)
        self.setLayout(self.layout)
        

    def setRemoveMode(self):
        if self.remove_mode:
            print("off")
            self.remove_mode = False
            self.remove_button.setStyleSheet(f"background-color:{Colors.base_color_05}")
        else :
            self.remove_mode = True
            self.remove_button.setStyleSheet(f"background-color:{Colors.buttonColor_01_select}")
            print("on")

    def openFileExplorer(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filters = "이미지 파일 (*.bmp *.dng *.jpeg *.jpg *.mpo *.png *.tif *.tiff *.webp *.pnm)"
        fname = QFileDialog()
        fname.setFileMode(QFileDialog.ExistingFiles)
        fname.setNameFilter(filters)
        if fname.exec_():
            selected_files = fname.selectedFiles()
            file_list = list()
            # Process selected files
            for file_path in selected_files:
                _, extension = os.path.splitext(file_path)
                if extension.lower() in ['.bmp', '.dng', '.jpeg', '.jpg', '.mpo', '.png', '.tif', '.tiff', '.webp', '.pnm']:
                    file_info = QUrl.fromLocalFile(file_path)
                    file_list.append(file_info)
            self.add_file.emit(file_list)

    def addNewFile(self, urls):
        for i, file_info in enumerate(urls):
            file_widget = ImageItem(file_info)
            file_widget.delet_signal.connect(self.removeFile)
            file_widget.doubleclick_signal.connect(self.itemDoubleClicked)
            file_widget.setFixedSize(120, 120)
            self.scroll_layout.addWidget(file_widget)
            self.count += 1

    def removeFile(self, widget):
        if self.remove_mode:
            self.remove_file.emit(widget.getUrl())
            self.scroll_layout.removeWidget(widget)
            widget.deleteLater()
        else :
            self.image_change.emit(widget.getUrl())

    def find_image(self, mimedata):
        self.urls = list()
        db = QMimeDatabase()
        allowed_extensions = ['image/bmp', 'image/x-adobe-dng', 'image/jpeg',
                               'image/jpg', 'image/mpo', 'image/png', 'image/tif',
                                'image/tiff', 'image/webp', 'image/x-portable-floatmap']
        for url in mimedata.urls():
            mimetype = db.mimeTypeForUrl(url)
            if mimetype.name() in allowed_extensions:
                self.urls.append(url)
        return self.urls
    
    #파일 끌어오기
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    #파일 놓기
    def dropEvent(self, event: QDragEnterEvent):
        urls = self.find_image(event.mimeData())
        
        if urls:
            self.drop_signal.emit(self.urls)
            event.accept()
        else:
            event.ignore()

    def getUrls(self):
        return self.urls
    
    def itemDoubleClicked(self, url):
        if not self.remove_mode:
            self.show_image(url)

    def show_image(self, file_path):
        if file_path:
            self.open_file(file_path)
        else:
            QMessageBox.critical(self, "Error", "Failed to load image")
    
    def open_file(self, file_path):
        QDesktopServices.openUrl(file_path)

