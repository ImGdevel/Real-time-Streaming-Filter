from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QMessageBox 
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtCore import QUrl, Qt, QFileInfo, Signal
import os

class ImageItem(QWidget):
    delet_signal = Signal(QWidget)
    doubleclick_signal = Signal(QUrl)
    def __init__(self, file_info):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.file_data = file_info
        file_url = file_info.toLocalFile()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap(file_url).scaled(80, 80))
        self.image_label.setFixedSize(80,80)

        self.name_label = QLabel(file_info.fileName())
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setFixedSize(80,20)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)

        self.setLayout(layout)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:  # 왼쪽 버튼 더블 클릭 확인
            self.doubleclick_signal.emit(self.file_data)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.delet_signal.emit(self)
    
    def getUrl(self):
        return self.file_data
    
class FaceImageItem(QWidget):
    delet_signal = Signal(QWidget)
    def __init__(self, file_info):
        super().__init__()
        self.file_data = file_info

        file_url = file_info.toLocalFile()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap(file_url).scaled(80, 80))
        self.image_label.setFixedSize(80,100)

        self.name_label = QLabel(file_info.fileName())
        self.name_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)

        self.setLayout(layout)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:  # 왼쪽 버튼 더블 클릭 확인
            self.show_image(self.file_data)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.delet_signal.emit(self)

    def show_image(self, file_path):
        if file_path:
            self.open_file(file_path)
        else:
            QMessageBox.critical(self, "Error", "Failed to load image")

    def open_file(self, file_path):
        QDesktopServices.openUrl(file_path)
    
    def getUrl(self):
        return self.file_data