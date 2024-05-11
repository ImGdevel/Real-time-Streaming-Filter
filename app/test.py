import sys
import numpy as np
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFrame, QSlider
from PySide6.QtGui import QImage, QPixmap, QPainter, QTransform
from PySide6.QtWidgets import QFileDialog
import cv2

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("이미지 뷰어 및 편집기")
        self.setGeometry(100, 100, 600, 700)  # 전체 창 크기 수정

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_frame = QFrame()
        self.image_frame.setFixedSize(400, 400)  # 이미지 뷰 크기 수정
        self.image_frame.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.image_frame)

        self.image_layout = QVBoxLayout()
        self.image_layout.setContentsMargins(0, 0, 0, 0)  # 마진 설정
        self.image_frame.setLayout(self.image_layout)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.image_label)

        self.load_button = QPushButton("이미지 불러오기")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.save_button = QPushButton("이미지 저장")
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)
        
        self.x_offset_slider = QSlider(Qt.Horizontal)
        self.x_offset_slider.setMaximum(400)
        self.x_offset_slider.setMinimum(-400)
        self.x_offset_slider.setValue(0)
        self.x_offset_slider.setTickInterval(10)
        self.x_offset_slider.valueChanged.connect(self.update_x_offset)
        self.layout.addWidget(self.x_offset_slider)

        self.y_offset_slider = QSlider(Qt.Horizontal)
        self.y_offset_slider.setMaximum(400)
        self.y_offset_slider.setMinimum(-400)
        self.y_offset_slider.setValue(0)
        self.y_offset_slider.setTickInterval(10)
        self.y_offset_slider.valueChanged.connect(self.update_y_offset)
        self.layout.addWidget(self.y_offset_slider)

        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMaximum(200)
        self.scale_slider.setMinimum(10)
        self.scale_slider.setValue(100)
        self.scale_slider.setTickInterval(10)
        self.scale_slider.valueChanged.connect(self.update_scale)
        self.layout.addWidget(self.scale_slider)

        self.origin_image = None  # 원본 이미지 저장용 변수
        self.edit_image = None  # 편집된 이미지 저장용 변수
        self.offset = QPoint()  # 이미지 이동을 위한 마우스 클릭 시 좌표 저장

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filename:
            image = QPixmap(filename)
            if image is None or image.width() == 0:
                raise ValueError("image error")
        
            self.origin_image = image
            self.edit_image = image.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.aspect_ratio = (image.width() / self.edit_image.width())
            self.image_scale = 1
            self.image_posX = 0
            self.image_posY = 0
            print("Image 비율")
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
        img = self.edit_image_set(self.edit_image, 400 , 400, self.image_posX, self.image_posY, self.image_scale)
        pixmap = QPixmap.fromImage(img)
        self.show_image(pixmap)

    def show_image(self, image : QPixmap):
        img  = image.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(img)
            
    def save_image(self):
        if self.origin_image:
            print("이미지 저장")
            self.origin_image.width()
            
            img = self.edit_image_set(self.origin_image, self.origin_image.width(), self.origin_image.width(), self.image_posX * self.aspect_ratio, self.image_posY * self.aspect_ratio, self.image_scale)
            img.save("output_image.png", "PNG")
            
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
                
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec())
