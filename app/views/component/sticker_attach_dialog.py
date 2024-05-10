from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLineEdit, QLabel, QFileDialog, QWidget
)
from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon, QImage
from models import StickerManager
from .title_bar import TitleBar
from utils import Style, Icons
import cv2
import numpy as np

class StickerRegisteredDialog(QDialog):
    onEventSave = Signal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Style.dialog_style)
        self.replace_manager = StickerManager()
        self.person_id = None
        self._initUI()

    def _initUI(self):
        self.setWindowTitle("Registered Face View")
        self.setFixedSize(400, 355)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 새로운 타이틀 바 생성
        self.title_bar = TitleBar(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.title_bar.setFixedHeight(40)
        
        content = QWidget()
        content.setStyleSheet(Style.frame_style)
        content_layout = QHBoxLayout()

        register_button = QPushButton()
        register_button.setIcon(QIcon(Icons.folder_open))
        register_button.setFixedSize(40, 40)
        register_button.clicked.connect(self.open_image)
        

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet("border: 2px solid #808080")
        
        set_frame = QWidget()
        
        save_button = QPushButton("등록")
        save_button.setFixedSize(50,50)
        save_button.setStyleSheet(Style.mini_button_style)
        save_button.clicked.connect(self.save)

        cancel_button = QPushButton("취소")
        cancel_button.setStyleSheet(Style.mini_button_style)
        cancel_button.setFixedSize(50,50)
        cancel_button.clicked.connect(self.cancel)
        
        button_layout = QGridLayout()
        button_layout.addWidget(save_button,0,0)
        button_layout.addWidget(cancel_button,1,0)
        set_frame.setLayout(button_layout)
        
        content_layout.addWidget(self.image_label)
        content_layout.addWidget(set_frame)
        content.setLayout(content_layout)
        
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content)

        self.setLayout(main_layout)

    def set_sticker_dialog(self, person_id, sticker_id):
        """이미 등록된 스티커가 있다면 불러오기"""
        self.person_id = person_id
        print(person_id, sticker_id)
        if sticker_id != -1:
            img = self.replace_manager.load_Qimg_to_id(sticker_id)
            if img is not None:
                pixmap = QPixmap.fromImage(img)
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(True)

    def open_image(self):
        """이미지 등록"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpeg)", options=options
        )

        if file_path:
            self.image_path = file_path
            self.load_image(file_path)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    def save(self):
        if hasattr(self, 'image_path'):
            sticker_id = self.replace_manager.register_img_path(self.image_path)
            self.onEventSave.emit(self.person_id, sticker_id)
        self.close()

    def cancel(self):
        self.close()
