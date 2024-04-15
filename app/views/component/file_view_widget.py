from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from utils.colors import Colors
from .image_item import ImageItem
import os

class FileViewWidget(QWidget):
    count = int
    remove_file = pyqtSignal(QUrl)
    add_file = pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.remove_mode = False
        self.count = 0
        self.layout = QVBoxLayout()
        #file view
        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.file_view_widget = QWidget()
        self.scroll_widget = QWidget()
        self.file_box_layout = QHBoxLayout()
        self.scroll_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.file_box_layout.addWidget(self.scroll_area)
        self.file_view_widget.setLayout(self.file_box_layout)

        #button
        self.button_widget = QWidget()
        self.button_widget.setFixedSize(300, 50)
        self.button_layout = QHBoxLayout()

        self.remove_button = QPushButton("Del = OFF")
        self.remove_button.clicked.connect(self.setRemoveMode)
        
        self.file_explorer_button = QPushButton("Serch")
        self.file_explorer_button.clicked.connect(self.openFileExplorer)
        
        self.button_layout.addWidget(self.remove_button)
        self.button_layout.addWidget(self.file_explorer_button)
        self.button_widget.setLayout(self.button_layout)

        #set frame layout
        self.layout.addWidget(self.file_view_widget)
        self.layout.addWidget(self.button_widget)
        self.setLayout(self.layout)
        

    def setRemoveMode(self):
        if self.remove_mode:
            print("off")
            self.remove_mode = False
            self.remove_button.setText("Del = OFF")
        else :
            self.remove_mode = True
            self.remove_button.setText("Del = ON")
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
            file_widget.setFixedSize(100, 100)
            self.scroll_layout.addWidget(file_widget)
            self.count += 1

    def removeFile(self, widget):
        self.remove_file.emit(widget.getUrl())
        if self.remove_mode:
            self.scroll_layout.removeWidget(widget)
            widget.deleteLater()


