from PySide6.QtCore import Qt, Signal, QTimer, QRectF, QSize
from PySide6.QtGui import QImage, QPixmap, QColor, QPainter
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QMessageBox, QSizePolicy
from utils import Colors, Icons

class SpinnerLoading(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)  # 위젯의 크기 설정
        self.angle = 0
        self.pixmap = QPixmap(Icons.loading)  # 이미지 로드
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.is_spin = False
        self.hide()  # 초기에는 이미지를 숨김

    def start(self):
        self.is_spin = True
        self.angle = 0  # 각도 초기화
        self.show()  # 이미지를 보임
        self.timer.start(10)  # 타이머 시작

    def stop(self):
        self.is_spin = False
        self.timer.stop()  # 타이머 멈춤
        self.hide()  # 이미지를 숨김

    def rotate(self):
        self.angle = (self.angle + 10) % 360  # 각도를 10도씩 증가시키며 360도에서 다시 0도로
        self.update()

    def paintEvent(self, event):
        if self.isHidden():
            return  # 이미지가 숨겨져 있으면 그리지 않음

        # 페인터 설정
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)  # 이미지 변환 시 부드럽게

        # 중심점 설정
        center = self.rect().center()
        
        # 이미지를 중심점 기준으로 회전
        painter.translate(center)
        painter.rotate(self.angle)
        painter.translate(-center)

        # 이미지를 그림
        rect = QRectF(self.pixmap.rect())
        rect.moveCenter(center)
        painter.drawPixmap(rect.topLeft(), self.pixmap)
        
        painter.end()