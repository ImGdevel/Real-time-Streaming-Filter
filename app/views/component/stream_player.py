from PySide6.QtCore import  Qt, QPoint, QRect
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from utils import Colors

class StreamVideoPlayer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.is_setInitWindowSize = False
        self.initUI()

    def initUI(self):
        video_layout = QHBoxLayout()

        self.video_box = QLabel()  # 비디오 플레이어 레이블
        self.video_box.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 배경색 및 테두리 설정
        self.video_box.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 정렬 설정
        video_layout.addWidget(self.video_box)
        self.video_box.setMaximumWidth(725)

        self.setLayout(video_layout)


    def update_video(self, frame: QImage = None):
        '''비디오 업데이트 메서드'''
        if frame is None:
            return
        pixmap = QPixmap.fromImage(frame)
        self.video_box.setPixmap(pixmap.scaled(self.video_box.width(), self.video_box.height(), Qt.KeepAspectRatio))

    
    def mousePressEvent(self, event):
        return
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.position().toPoint()
            self.drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        return
        if self.drawing:
            self.end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        return
        if event.button() == Qt.MouseButton.LeftButton:
            self.end_point = event.position().toPoint()
            self.drawing = False
            self.update()

    def paintEvent(self, event):
        return
        if self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start_point, self.end_point)
            painter.drawRect(rect)





    # def enterEvent(self, event):
        
    #     if self.temp_mode:
    #         self.video_box.setCursor(Qt.CrossCursor)

    # def mousePressEvent(self, event):
    #     if self.temp_mode:
    #         current_point = QPoint(self.image_posX, self.image_posY)
    #         self.offset = event.globalPosition() - current_point

    # def mouseMoveEvent(self, event):
    #     if self.temp_mode:
    #         self.new_pos = event.globalPosition() - self.offset
    #         self.image_posX = self.new_pos.x()
    #         self.image_posY = self.new_pos.y()

    # def mouseReleaseEvent(self, event):
    #     if self.temp_mode:
    #         #만약 영역을 벗어난 경우
    #         pass


    # def leaveEvent(self, event):
    #     pass
