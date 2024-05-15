from PySide6.QtWidgets import QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QMimeDatabase, Signal
from PySide6.QtGui import QPixmap, QDragEnterEvent, QImage, QResizeEvent
from urllib.parse import urlparse


class DragDropLabel(QLabel):

    drop_signal = Signal(list)
    currunt_exm = str()
    currunt_filt = str()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.currunt_exm = None
        self.currunt_filt = None
        self.layout = QHBoxLayout()
        self.dropbox_lable = QLabel()
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
        self.filtered_label.setAlignment(Qt.AlignCenter)
        self.filtered_label.setText('Filtered')
        self.filtered_label.setStyleSheet('''
            QLabel{
                    border: 4px dashed #aaa;
                    font-size: 15pt;
                    font-family:'Malgun Gothic';
            }
        ''')

        self.layout.addWidget(self.dropbox_lable, 1)
        self.layout.addWidget(self.filtered_label, 1)
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
        image = QImage(urls)
        
        # Check if the image has loaded successfully
        if image.isNull():
            print("Failed to load the image.")
            return
        
        pixmap = QPixmap.fromImage(image)
        widget_size = self.dropbox_lable.size()
        print(widget_size)
        # Get image size
        image_size = pixmap.size()

        # Calculate scaling factor to fit the image into the widget
        width_factor = widget_size.width() / image_size.width()
        height_factor = widget_size.height() / image_size.height()

        # Choose the smallest scaling factor to maintain aspect ratio
        scale_factor = min(width_factor, height_factor)
        print("factor ",scale_factor)

        # Scale pixmap with maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(int(image_size.width() * scale_factor) - 15, 
                                    int(image_size.height() * scale_factor) - 15, 
                                    Qt.KeepAspectRatio)

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
        scaled_pixmap = pixmap.scaled(int(image_size.width() * scale_factor) -15, 
                                    int(image_size.height() * scale_factor) -15, 
                                    Qt.KeepAspectRatio)

        self.filtered_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event: QResizeEvent) -> None:
        frame_size = self.size()
        self.dropbox_lable.resize(frame_size.width()/2 - 15, frame_size.height() - 15)
        self.refreashWidget()
        return super().resizeEvent(event)
    
    def refreashWidget(self):
        if self.currunt_exm:
            self.setExampleView(self.currunt_exm)
            print("refreashed")
        if self.currunt_filt:
            self.setFilteredView(self.currunt_filt)
    
    def emptyExmLabel(self):
        self.dropbox_lable.clear()
        self.dropbox_lable.setText('Original')

    def emptyFiletLabel(self):
        self.filtered_label.clear()
        self.filtered_label.setText('Filtered')

