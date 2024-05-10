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
        
        self.crop_button = QPushButton("잘라내기")
        self.crop_button.clicked.connect(self.crop_image)
        self.layout.addWidget(self.crop_button)
        
        self.reset_button = QPushButton("초기화")
        self.reset_button.clicked.connect(self.reset_image)
        self.layout.addWidget(self.reset_button)

        # # 슬라이더 추가
        # self.slider_x = QSlider(Qt.Horizontal)
        # self.slider_x.setMinimum(-200)
        # self.slider_x.setMaximum(200)
        # self.slider_x.setValue(0)
        # self.slider_x.setTickInterval(10)
        # self.slider_x.setTickPosition(QSlider.TicksBelow)
        # self.slider_x.valueChanged.connect(self.update_image_position)
        # self.layout.addWidget(self.slider_x)

        # self.slider_y = QSlider(Qt.Horizontal)
        # self.slider_y.setMinimum(-200)
        # self.slider_y.setMaximum(200)
        # self.slider_y.setValue(0)
        # self.slider_y.setTickInterval(10)
        # self.slider_y.setTickPosition(QSlider.TicksBelow)
        # self.slider_y.valueChanged.connect(self.update_image_position)
        # self.layout.addWidget(self.slider_y)

        # self.slider_scale = QSlider(Qt.Horizontal)
        # self.slider_scale.setMinimum(1)
        # self.slider_scale.setMaximum(3)
        # self.slider_scale.setValue(1)
        # self.slider_scale.setTickInterval(0.1)
        # self.slider_scale.setTickPosition(QSlider.TicksBelow)
        # self.slider_scale.valueChanged.connect(self.update_image_scale)
        # self.layout.addWidget(self.slider_scale)

        self.edit_image = None  # 원본 이미지 저장용 변수
        self.edit_image = None  # 편집된 이미지 저장용 변수
        self.offset = QPoint()  # 이미지 이동을 위한 마우스 클릭 시 좌표 저장

        # 이미지 위치 및 크기 변수
        self.image_posX = 0
        self.image_posY = 0
        self.image_scale = 1.0

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filename:
            image = QPixmap(filename)
            image_scaled = image.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.origin_image = image
            self.edit_image = image_scaled
            self.image_posX = 0
            self.image_posY = 0
            self.image_scale = 0.4
            self.show_image()


    def save_image(self):
        if self.edit_image:
            file_path, _ = QFileDialog.getSaveFileName(self, "이미지 저장", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)")
            if file_path:
                self.edit_image.save(file_path)

    def crop_image(self):
        if self.edit_image:
            # 이미지의 크기를 계산합니다.
            image_width = int(self.edit_image.width() * self.image_scale)
            image_height = int(self.edit_image.height() * self.image_scale)

            # 잘라낼 영역의 크기를 계산합니다.
            crop_width = min(self.image_frame.width(), image_width - self.image_posX)
            crop_height = min(self.image_frame.height(), image_height - self.image_posY)

            # 잘라낸 이미지를 얻습니다.
            cropped_image = self.edit_image.copy(self.image_posX, self.image_posY, crop_width, crop_height)

            # 잘라낸 이미지를 보여줍니다.
            self.image_label.setPixmap(cropped_image)

            # 잘라낸 이미지를 edit_image에 저장하여 다음 작업에 사용합니다.
            self.cut_image = cropped_image
            
            print("수정된 이미지", self.edit_image)
            
            
    def crop_and_fill(image, target_size = 400):
        # 이미지를 원하는 크기로 잘라냅니다.
        cropped_image = image.copy(0, 0, target_size.width(), target_size.height())
        
        # 새로운 크기로 이미지를 만듭니다.
        new_image = QPixmap(target_size)
        new_image.fill(Qt.transparent)  # 투명한 알파값으로 초기화합니다.
        
        # 잘라낸 이미지를 새로운 이미지의 원하는 위치에 붙여넣습니다.
        painter = QPainter(new_image)
        painter.drawPixmap((target_size.width() - cropped_image.width()) // 2, (target_size.height() - cropped_image.height()) // 2, cropped_image)
        painter.end()
        
        return new_image
                
    def reset_image(self):
        if self.edit_image:
            # 원본 이미지로 되돌립니다.
            self.edit_image = self.origin_image
            self.show_image()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.offset = event.globalPosition() - self.image_label.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.edit_image:
            self.new_pos = event.globalPosition() - self.offset
            self.image_posX = self.new_pos.x()
            self.image_posY = self.new_pos.y()
            self.update_image_position()

    def wheelEvent(self, event):
        if self.edit_image:
            delta = event.angleDelta().y() / 120
            if delta > 0:
                # 휠을 위로 굴리면 이미지 확대
                self.image_scale *= 1.1
            else:
                # 휠을 아래로 굴리면 이미지 축소
                self.image_scale *= 0.9
            self.update_image_scale()

    def update_image_scale(self):
        # 슬라이더 값을 기반으로 이미지를 확대 또는 축소합니다.
        transform = QTransform().translate(self.image_posX, self.image_posY).scale(self.image_scale, self.image_scale).rotate(180)
        transformed_pixmap = self.origin_image.transformed(transform, Qt.SmoothTransformation)
        
        print(transformed_pixmap)
        self.edit_image = transformed_pixmap
        self.image_label.setPixmap(self.edit_image)
        self.image_label.move(self.image_posX, self.image_posY)

    def update_image_position(self):
        # 슬라이더 값을 기반으로 이미지의 위치를 업데이트합니다.
        self.image_label.move(self.image_posX, self.image_posY)
        
    def show_image(self):
        self.image_label.setPixmap(self.edit_image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec())
