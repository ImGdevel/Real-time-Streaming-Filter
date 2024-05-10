import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QColor
from utils import Icons

class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로딩중")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor(0, 0, 0))  # 배경색을 검은색으로 설정

        self.graphics_view = QGraphicsView(self.scene)
        layout.addWidget(self.graphics_view)

        # Icons 모듈에서 로딩 이미지 경로를 가져와 QPixmap으로 변환
        loading_pixmap = QPixmap(Icons.loading)
        self.loading_item = QGraphicsPixmapItem(loading_pixmap)
        self.scene.addItem(self.loading_item)

        # 중심점을 설정하여 이미지가 로테이션 될 때 중심이 고정되도록 함
        self.loading_item.setTransformOriginPoint(loading_pixmap.width() / 2, loading_pixmap.height() / 2)

        # 회전 각도 초기화
        self.rotation_angle = 0

        # 타이머 설정하여 이미지 회전
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_image)
        self.timer.start(10)  # 10 milliseconds마다 이미지를 회전시킴

        # 종료 버튼 추가
        self.close_button = QPushButton("종료")
        self.close_button.clicked.connect(self.close_window)
        layout.addWidget(self.close_button)

    def rotate_image(self):
        # 회전 각도를 증가시켜 이미지를 회전시킴
        self.rotation_angle += 5
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.loading_item.setRotation(self.rotation_angle)

    def close_window(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("메인 윈도우")
        self.setGeometry(100, 100, 400, 200)

        self.loading_window = None

        # Loading 윈도우를 시작하는 버튼
        self.start_loading_button = QPushButton("로딩 시작")
        self.start_loading_button.clicked.connect(self.start_loading)
        self.setCentralWidget(self.start_loading_button)

    def start_loading(self):
        # Loading 윈도우를 생성하고 표시
        self.loading_window = LoadingWindow()
        self.loading_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
