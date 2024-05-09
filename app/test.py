import sys
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFrame
from PySide6.QtGui import QImage, QPixmap, QPainter, QTransform
from PySide6.QtWidgets import QFileDialog

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("이미지 뷰어 및 편집기")
        self.setGeometry(100, 100, 500, 600)  # 전체 창 크기 수정

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

        self.my_image = None  # 이미지 저장용 변수
        self.offset = QPoint()  # 이미지 이동을 위한 마우스 클릭 시 좌표 저장

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filename:
            image = QImage(filename)
            image_scaled = image.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation, interpolationMode=Qt.HighQualityAntialiasing ) # 비율 유지 및 보간 설정
            self.image_label.setPixmap(QPixmap.fromImage(image_scaled))
            self.my_image = image_scaled  # 이미지 저장

    def save_image(self):
        if self.my_image:
            file_path, _ = QFileDialog.getSaveFileName(self, "이미지 저장", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)")
            if file_path:
                self.my_image.save(file_path)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.offset = event.globalPos() - self.image_label.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.my_image:
            new_pos = event.globalPos() - self.offset
            self.image_label.move(new_pos)

    def wheelEvent(self, event):
        if self.my_image:
            delta = event.angleDelta().y() / 120
            if delta > 0:
                # 휠을 위로 굴리면 이미지 확대
                transform = QTransform().scale(1.1, 1.1)
            else:
                # 휠을 아래로 굴리면 이미지 축소
                transform = QTransform().scale(0.9, 0.9)
            self.my_image = self.my_image.transformed(transform, Qt.SmoothTransformation)
            self.image_label.setPixmap(QPixmap.fromImage(self.my_image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())
