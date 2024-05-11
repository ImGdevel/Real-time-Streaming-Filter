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

        self.edit_image = None  # 원본 이미지 저장용 변수
        self.edit_image = None  # 편집된 이미지 저장용 변수
        self.offset = QPoint()  # 이미지 이동을 위한 마우스 클릭 시 좌표 저장

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filename:
            image = QPixmap(filename)
            if image is None or image.width() == 0:
                raise ValueError("image error")
        
            image_scaled = image.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.origin_image = image
            self.edit_image = image_scaled
            self.image_scale = (image_scaled.width() / image.width()) 
            self.image_posX = 0
            self.image_posY = 0
            print("Image 비율")
            self.show_image(image_scaled)


    
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.offset = event.globalPosition() - self.image_label.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.edit_image:
            self.new_pos = event.globalPosition() - self.offset
            self.image_posX = self.new_pos.x()
            self.image_posY = self.new_pos.y()

    def wheelEvent(self, event):
        if self.edit_image:
            delta = event.angleDelta().y() / 120
            if delta > 0:
                # 휠을 위로 굴리면 이미지 확대
                self.image_scale *= 1.1
            else:
                # 휠을 아래로 굴리면 이미지 축소
                self.image_scale *= 0.9
            
    def applay_image(self):
        pass
        
            
    def show_image(self, img : QPixmap):
        self.image_label.setPixmap(img)
        
            
    def save_image(self, img: QImage):
        if img:
            print(self.image_posX, "/" ,self.image_posY, "/", self.image_scale)
            img = self.edit_image(self.origin_image, self.image_label , self.image_label, self.image_posX, self.image_posY, self.image_scale)
            img.save("output_image", "png")
            
    def edit_image(input_image_path : QPixmap, width, height, x_offset: int = 0, y_offset : int = 0, scale : float = 1)  -> QImage:
        # Load input image
        original_image = input_image_path

        # Scale the image
        scaled_image = original_image.scaled(original_image.width() * scale, original_image.height() * scale, Qt.KeepAspectRatio)

        # Create a new image with transparent background
        new_image = QImage(width, height, QImage.Format_ARGB32)
        new_image.fill(Qt.transparent)

        # Calculate the position to paste the scaled image
        paste_x = (width - scaled_image.width()) // 2 + x_offset
        paste_y = (height - scaled_image.height()) // 2 + y_offset

        # Create a QPainter object for the new image
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
