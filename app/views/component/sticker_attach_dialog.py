from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget, QSlider
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QGridLayout, QSpacerItem, QListWidgetItem, QProgressDialog
from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication, QPoint
from PySide6.QtGui import QPixmap, QIcon, QImage, QPainter
from models import StickerManager
from .title_bar import TitleBar
from utils import Style, Icons
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
        self.setFixedSize(660, 505)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 새로운 타이틀 바 생성
        self.title_bar = TitleBar(self)
        self.title_bar.set_title("얼굴 스티커 등록")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.title_bar.setFixedHeight(40)
        
        content = QWidget()
        content.setStyleSheet(Style.frame_style)
        content_layout = QHBoxLayout()

        register_button = QPushButton()
        register_button.setIcon(QIcon(Icons.folder_open))
        register_button.setFixedSize(40, 40)
        register_button.clicked.connect(self.load_image)

        self.image_label = QLabel()
        self.image_label.setFixedSize(450, 450)
        self.image_label.setStyleSheet("border: 2px solid #808080")
        
        set_frame = QWidget()
        
        save_button = QPushButton("등록")
        save_button.setFixedHeight(30)
        save_button.setStyleSheet(Style.mini_button_style)
        save_button.clicked.connect(self.save_image)

        cancel_button = QPushButton("취소")
        cancel_button.setStyleSheet(Style.mini_button_style)
        cancel_button.setFixedHeight(30)
        cancel_button.clicked.connect(self.cancel)
        
        self.x_offset_slider = QSlider(Qt.Horizontal)
        self.x_offset_slider.setMaximum(200)
        self.x_offset_slider.setMinimum(-200)
        self.x_offset_slider.setValue(0)
        self.x_offset_slider.setTickInterval(10)
        self.x_offset_slider.valueChanged.connect(self.update_x_offset)
        

        self.y_offset_slider = QSlider(Qt.Horizontal)
        self.y_offset_slider.setMaximum(200)
        self.y_offset_slider.setMinimum(-200)
        self.y_offset_slider.setValue(0)
        self.y_offset_slider.setTickInterval(10)
        self.y_offset_slider.valueChanged.connect(self.update_y_offset)
        

        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMaximum(200)
        self.scale_slider.setMinimum(10)
        self.scale_slider.setValue(100)
        self.scale_slider.setTickInterval(10)
        self.scale_slider.valueChanged.connect(self.update_scale)
        

        self.origin_image = None  # 원본 이미지 저장용 변수
        self.edit_image = None  # 편집된 이미지 저장용 변수
        self.offset = QPoint()  # 이미지 이동을 위한 마우스 클릭 시 좌표 저장
        
        button_layout = QGridLayout()
        button_layout.addWidget(register_button,0,0)
        button_layout.addWidget(self.x_offset_slider,1,0)
        button_layout.addWidget(self.y_offset_slider,2,0)
        button_layout.addWidget(self.scale_slider,3,0)
        button_layout.addWidget(save_button,4,0)
        button_layout.addWidget(cancel_button,5,0)
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
                self.init_image(pixmap)

    def save_image(self):
        if self.edit_image:
            img = self.edit_image_set(self.edit_image, self.image_label.width(), self.image_label.height(), self.image_posX, self.image_posY , self.image_scale)
            nparry_img = self.qimage_to_cv_image(img)
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
            self.init_image(image)

    def init_image(self, image : QPixmap):
        self.is_sticker_seletecd = True
        self.origin_image = image
        self.edit_image = image.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.aspect_ratio = (image.width() / self.edit_image.width())
        self.image_scale = 1
        self.image_posX = 0
        self.image_posY = 0
        self.show_image(image)
        
            
    def update_x_offset(self, value):
        if self.origin_image:
            self.image_posX = value
            self.applay_image()

    def update_y_offset(self, value):
        if self.origin_image:
            self.image_posY = value
            self.applay_image()

    def update_scale(self, value):
        if self.origin_image:
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
        if self.edit_image:
            img = self.edit_image_set(self.edit_image, self.image_label.width(), self.image_label.height(), self.image_posX, self.image_posY, self.image_scale)
            pixmap = QPixmap.fromImage(img)
            self.show_image(pixmap)

    def show_image(self, image : QPixmap):
        img  = image.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(img)
            
    def edit_image_set(self, input_image : QPixmap, width : int, height : int, 
                       x_offset: int = 0, y_offset : int = 0, scale : float = 1)  -> QImage:
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
    
    def qimage_to_cv_image(self, qimage: QImage):
        width = qimage.width()
        height = qimage.height()
        bytes_per_line = qimage.bytesPerLine()
        image_format = qimage.format()

        if image_format == QImage.Format_ARGB32 or image_format == QImage.Format_RGB32:
            # QImage에서 numpy 배열로 직접 변환합니다.
            ptr = qimage.bits()
            arr = np.array(ptr).reshape((height, width, 4))  # 4 채널(알파 포함) 이미지
        else:
            # 포맷이 다를 경우 QImage를 ARGB32 포맷으로 변환합니다.
            qimage = qimage.convertToFormat(QImage.Format_ARGB32)
            ptr = qimage.bits()
            arr = np.array(ptr).reshape((height, width, 4))  # 4 채널(알파 포함) 이미지

        # OpenCV 형식으로 변환합니다. (BGR 형식)
        #cv_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA)
        return arr