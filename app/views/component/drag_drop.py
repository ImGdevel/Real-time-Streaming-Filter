from PyQt5.QtWidgets import QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QMimeDatabase, pyqtSignal
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QImage
from utils import Colors
from urllib.parse import urlparse


class DragDropLabel(QLabel):

    drop_signal = pyqtSignal(list)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.dropbox_lable = QLabel()
        self.dropbox_lable.setFixedSize(378, 412)
        self.dropbox_lable.setAlignment(Qt.AlignCenter)
        self.dropbox_lable.setText('Original')
        self.dropbox_lable.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
                font-size: 15pt;
                font-family:'Malgun Gothic';
            }
        ''')

        self.filtered_label = QLabel()
        self.filtered_label.setFixedSize(378, 412)
        self.filtered_label.setAlignment(Qt.AlignCenter)
        self.filtered_label.setText('Filtered')
        self.filtered_label.setStyleSheet('''
            QLabel{
                    border: 4px dashed #aaa;
                    font-size: 15pt;
                    font-family:'Malgun Gothic';
            }
        ''')


        self.layout.addWidget(self.dropbox_lable)
        self.layout.addWidget(self.filtered_label)
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
        print(widget_size)
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

    def setFilteredView(self, image_path):
        # Load an image from the given path
        image = QImage(image_path)
        
        # Check if the image has loaded successfully
        if image.isNull():
            print("Failed to load the image.")
            return
        
        # Convert QImage to QPixmap for display
        pixmap = QPixmap.fromImage(image)

        # Get the size of the widget where the image will be displayed
        widget_size = self.filtered_label.size()
        print(widget_size)

        # Get image size from the QPixmap
        image_size = pixmap.size()

        # Calculate scaling factor to fit the image into the widget
        width_factor = widget_size.width() / image_size.width()
        height_factor = widget_size.height() / image_size.height()

        # Choose the smallest scaling factor to maintain aspect ratio
        scale_factor = min(width_factor, height_factor)

        # Scale pixmap while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(int(image_size.width() * scale_factor), 
                                    int(image_size.height() * scale_factor), 
                                    Qt.KeepAspectRatio)

        self.filtered_label.setPixmap(scaled_pixmap)
