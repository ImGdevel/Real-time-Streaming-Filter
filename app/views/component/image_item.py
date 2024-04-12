from PyQt5.QtWidgets import QLabel, QWidget, QFileIconProvider, QVBoxLayout, QMessageBox 
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, Qt, QFileInfo, pyqtSignal

class ImageItem(QWidget):
    delet_signal = pyqtSignal(QWidget)
    def __init__(self, file_info):
        super().__init__()
        self.file_data = file_info
        icon_provider = QFileIconProvider()

        file_url = QFileInfo(QUrl.toLocalFile(file_info))
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(icon_provider.icon(file_url).pixmap(32, 32))

        self.name_label = QLabel()
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