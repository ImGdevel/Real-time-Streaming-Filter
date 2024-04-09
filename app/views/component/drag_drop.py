from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeDatabase
from utils import Colors


class DragDropLabel(QLabel):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.dropbox_lable = QLabel()
        self.dropbox_lable.setMinimumSize(500, 300)
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
    def dragEnterEvent(self, event):
        print("Drag in")

    #파일 놓기
    def dropEvent(self, event):
        urls = self.find_image(event.mimeData())
        if urls:
            for url in urls:
                print(url.toLocalFile())
            event.accept()
        else:
            event.ignore()

    def getUrls(self):
        return self.urls