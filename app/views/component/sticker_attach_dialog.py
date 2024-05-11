from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget, QSlider
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QGridLayout, QSpacerItem, QListWidgetItem, QProgressDialog
from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication, QPoint
from PySide6.QtGui import QPixmap, QIcon, QImage, QPainter
from models import StickerManager
from utils import Style, Icons
import cv2
import numpy as np
import qimage2ndarray

class StickerRegisteredDialog(QDialog):
    onEventSave = Signal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Style.frame_style)
        self.replace_manager = StickerManager()
        self.person_id = None
        self._initUI()

    def _initUI(self):
        self.setWindowTitle("Registered Face View")
        self.setFixedSize(320, 400)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        register_button = QPushButton()
        register_button.setStyleSheet("border: 2px solid #808080; padding: 5px")
        register_button.setIcon(QIcon(Icons.folder_open))
        register_button.setFixedSize(40, 40)
        register_button.clicked.connect(self.load_image)
        main_layout.addWidget(register_button)

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet("border: 2px solid #808080")
        main_layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        save_button = QPushButton("등록")
        save_button.setStyleSheet("border: 2px solid #808080; padding: 5px")
        save_button.clicked.connect(self.save_image)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("취소")
        cancel_button.setStyleSheet("border: 2px solid #808080; padding: 5px")
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)
        
        self.x_offset_slider = QSlider(Qt.Horizontal)
        self.x_offset_slider.setMaximum(400)
        self.x_offset_slider.setMinimum(-400)
        self.x_offset_slider.setValue(0)
        self.x_offset_slider.setTickInterval(10)
        self.x_offset_slider.valueChanged.connect(self.update_x_offset)
        button_layout.addWidget(self.x_offset_slider)

        self.y_offset_slider = QSlider(Qt.Horizontal)
        self.y_offset_slider.setMaximum(400)
        self.y_offset_slider.setMinimum(-400)
        self.y_offset_slider.setValue(0)
        self.y_offset_slider.setTickInterval(10)
        self.y_offset_slider.valueChanged.connect(self.update_y_offset)
        button_layout.addWidget(self.y_offset_slider)

        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMaximum(200)
        self.scale_slider.setMinimum(10)
        self.scale_slider.setValue(100)
        self.scale_slider.setTickInterval(10)
        self.scale_slider.valueChanged.connect(self.update_scale)
        button_layout.addWidget(self.scale_slider)

        self.origin_image = None  # 원본 이미지 저장용 변수
        self.edit_image = None  # 편집된 이미지 저장용 변수
        self.offset = QPoint()  # 이미지 이동을 위한 마우스 클릭 시 좌표 저장

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def set_sticker_dialog(self, person_id, sticker_id):
        """이미 등록된 스티커가 있다면 불러오기"""
        self.person_id = person_id
        print(person_id, sticker_id)
        if sticker_id != -1:
            img = self.replace_manager.load_Qimg_to_id(sticker_id)
            if img is not None:
                self.show_image(img)

    def save_image(self):
        if self.origin_image:
            print("이미지 저장")
            img = self.edit_image_set(self.origin_image, self.origin_image.width(), self.origin_image.width(), self.image_posX * self.aspect_ratio, self.image_posY * self.aspect_ratio, self.image_scale)

            nparry_img = self.qImage2array(img)
            sticker_id = self.replace_manager.register_img(nparry_img)
            self.onEventSave.emit(self.person_id, sticker_id)
            self.close()
        
    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filename:
            image = QPixmap(filename)
            if image is None or image.width() == 0:
                raise ValueError("image error")
        
            self.origin_image = image
            
            self.edit_image = image.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.aspect_ratio = (image.width() / self.edit_image.width())
            self.image_scale = 1
            self.image_posX = 0
            self.image_posY = 0
            self.show_image(image)
            
    def update_x_offset(self, value):
        self.image_posX = value
        self.applay_image()

    def update_y_offset(self, value):
        self.image_posY = value
        self.applay_image()

    def update_scale(self, value):
        self.image_scale = value / 100
        self.applay_image()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            current_point = QPoint(self.image_posX, self.image_posY)
            self.offset = event.globalPosition() - current_point

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.origin_image:
            self.new_pos = event.globalPosition() - self.offset
            self.image_posX = self.new_pos.x() 
            self.image_posY = self.new_pos.y()
            self.x_offset_slider.setValue(self.image_posX)
            self.y_offset_slider.setValue(self.image_posY)
            self.applay_image()

    def wheelEvent(self, event):
        if self.origin_image:
            delta = event.angleDelta().y() / 120
            if delta > 0:
                # 휠을 위로 굴리면 이미지 확대
                self.image_scale = round(self.image_scale * 1.1, 2)
            else:
                # 휠을 아래로 굴리면 이미지 축소
                self.image_scale = round(self.image_scale * 0.9, 2)
            self.scale_slider.setValue(self.image_scale * 100)
            self.applay_image()
            
    def applay_image(self):
        print("X(", self.image_posX, ")  Y(" ,self.image_posY, ") Scale(", self.image_scale , ")")
        img = self.edit_image_set(self.edit_image,self.image_label.width(), self.image_label.height(), self.image_posX, self.image_posY, self.image_scale)
        pixmap = QPixmap.fromImage(img)
        self.show_image(pixmap)

    def show_image(self, image : QPixmap):
        img  = image.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(img)
            
    def edit_image_set(self, input_image : QPixmap, width : int, height : int, x_offset: int = 0, y_offset : int = 0, scale : float = 1)  -> QImage:
        original_image = input_image

        scaled_image = original_image.scaled(original_image.width() * scale, original_image.height() * scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        new_image = QImage(width, height, QImage.Format_ARGB32)
        new_image.fill(Qt.transparent)

        paste_x = (width - scaled_image.width()) // 2 + x_offset
        paste_y = (height - scaled_image.height()) // 2 + y_offset

        painter = QPainter(new_image)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(paste_x, paste_y, scaled_image)
        painter.end()

        return new_image
    
    def cancel(self):
        self.close()

    # 이미지를 OpenCV 형식으로 변환하는 메소드
    def qImage2array(self, qimage : QImage):
        if  qimage.format() != QImage.Format_ARGB32:
                # QImage를 32비트 이미지로 변환
            qimage = qimage.convertToFormat(QImage.Format_ARGB32)

            img = qimage2ndarray.rgb_view(qimage)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
        
            return img