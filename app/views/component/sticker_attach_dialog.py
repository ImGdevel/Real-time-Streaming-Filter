from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QGridLayout, QSpacerItem, QListWidgetItem, QProgressDialog
from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon
from models.replace_manager import ReplaceManager
from utils import Style

class StickerAttachDialog(QDialog):
    updateEvent = Signal(int) 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Style.frame_style)
        self._initUI()

    def _initUI(self):
        self.setWindowTitle("Add Face")
        self.setFixedSize(320, 400)

        main_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet("border: 2px solid #808080")
        main_layout.addWidget(self.image_label)

        self.open_file_button = QPushButton("Open Image")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.open_file_button.setStyleSheet("border: 2px solid #808080; padding: 5px")
        main_layout.addWidget(self.open_file_button)

        self.setLayout(main_layout)
        
    def set_sticker_dialog(self, id = None):
        
        
        
        
        pass

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Open Images", "", "Image Files (*.png *.jpeg)", options=options
        )

        if file_paths:
            file_path = file_paths[0]
            self.load_image(file_path)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    def drag_enter_event(self, event):
        """드래그 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drag_move_event(self, event):
        """드래그 이동 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """드롭 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            
            image_files = [url.toLocalFile() for url in event.mimeData().urls()]
            self.add_face_process(image_files)
        else:
            event.ignore()

    def add_face_process(self, image_files):
        """이미지 등록 프로세스"""

        for idx, file_path in enumerate(image_files):
            if not self.current_person.face_name is None:
                pass
