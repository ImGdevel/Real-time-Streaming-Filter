from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeDatabase, pyqtSignal
from PyQt5.QtGui import QPixmap, QDragEnterEvent
from utils import Colors
from urllib.parse import urlparse


class DragDropLabel(QLabel):

    drop_signal = pyqtSignal(list)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.dropbox_lable = QLabel()
        #self.dropbox_lable.setMinimumSize(300, 150)
        #self.dropbox_lable.setMaximumWidth(550)
        self.dropbox_lable.setAlignment(Qt.AlignCenter)
        self.dropbox_lable.setText('파일을 끌어오세요')
        self.dropbox_lable.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
                font-size: 15pt;
                font-family:'Malgun Gothic';
            }
        ''')

        self.layout.addWidget(self.dropbox_lable)
        self.setLayout(self.layout)
        
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
    
    def setExampleView(self, urls):
        pixmap = QPixmap(urls)
        widget_size = self.dropbox_lable.size()
        # Get image size
        image_size = pixmap.size()

        # Calculate scaling factor to fit the image into the widget
        width_factor = widget_size.width() / image_size.width()
        height_factor = widget_size.height() / image_size.height()

        # Choose the smallest scaling factor to maintain aspect ratio
        scale_factor = min(width_factor, height_factor)

        # Scale pixmap with maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(image_size * scale_factor, Qt.KeepAspectRatio)

        self.dropbox_lable.setPixmap(scaled_pixmap)
