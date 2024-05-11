#체크포인트-002
import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFrame, QAction
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QFileDialog

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
        
        self.init_toolbar()  # 툴바 초기화 메서드 호출

    def init_toolbar(self):
        toolbar = self.addToolBar("Tool Bar")
        
        process_action = QAction("이미지 처리", self)
        process_action.triggered.connect(self.process_image)
        toolbar.addAction(process_action)
        
        
    def process_image(self):
        if self.my_image:
            # 이미지 사이즈를 0.5배로 조정
            scaled_image = self.my_image.scaled(int(self.my_image.width() * 0.5), int(self.my_image.height() * 0.5))

            # 이미지를 위로 50만큼 이동
            moved_image = scaled_image.copy()
            move_distance = 50
            moved_image.fill(Qt.black)  # 배경 채우기
            painter = QPainter(moved_image)
            painter.drawImage(0, move_distance, scaled_image)
            painter.end()
            
            print("이미지 처리 시도")

            # 중앙을 중심으로 400x400만큼 자르기
            if moved_image.width() > 400 and moved_image.height() > 400:
                crop_rect = QRect((moved_image.width() - 400) // 2, (moved_image.height() - 400) // 2, 400, 400)
                cropped_image = moved_image.copy(crop_rect)
                self.image_label.setPixmap(QPixmap.fromImage(cropped_image))
                self.my_image = cropped_image
                
                print("이미지 처리 완료")
                
            self.display_image(self.my_image)
                
    def display_image(self, image):
        if image:
            self.image_label.setPixmap(QPixmap.fromImage(image))
                
    def save_cropped_image(self, image):
        if image:
            # 이미지를 파일로 저장
            save_path, _ = QFileDialog.getSaveFileName(self, "이미지 저장", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)")
            if save_path:
                image.save(save_path)
                print(f"이미지가 {save_path}에 저장되었습니다.")
            else:
                print("이미지 저장이 취소되었습니다.")

    def load_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if filename:
            image = QImage(filename)
            image_scaled = image.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio)  # 비율 유지
            self.image_label.setPixmap(QPixmap.fromImage(image_scaled))
            self.my_image = image_scaled  # 이미지 저장

    def save_image(self):
        if self.my_image:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())