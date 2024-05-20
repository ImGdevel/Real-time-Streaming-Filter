from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QMessageBox
from utils import Colors
from .focus_detect_select_area import FocusDetectSelectArea

class StreamVideoPlayer(QWidget):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.focusSelectMode = False
        self.original_size : QSize = None
        self.current_size : QSize = None
        self.initUI()

    def initUI(self):
        video_layout = QHBoxLayout()

        self.show_box = QLabel()
        self.show_box.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.show_box.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        video_layout.addWidget(self.show_box)
        self.show_box.setMaximumWidth(725)

        # FocusDetectSelectArea를 show_box와 동일한 위치와 크기로 추가
        self.overlay = FocusDetectSelectArea(self.show_box)
        self.overlay.setGeometry(0, 0, self.show_box.width(), self.show_box.height())
        self.overlay.raise_()  # overlay를 맨 앞으로 가져옴

        # 신호 연결
        self.overlay.areaSelected.connect(self.handle_area_selected)

        self.setLayout(video_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # show_box가 리사이즈 될 때 overlay도 리사이즈
        self.overlay.setGeometry(0, 0, self.show_box.width(), self.show_box.height())

    def update_video(self, frame: QImage = None):
        '''비디오 업데이트 메서드'''
        if frame is None:
            return
        if self.original_size is None:
            self.original_size = frame.size()
        
        pixmap = QPixmap.fromImage(frame)
        self.show_box.setPixmap(pixmap.scaled(self.show_box.width(), self.show_box.height(), Qt.KeepAspectRatio))
        if self.current_size is None :
            self.current_size = QSize(self.show_box.width(), self.show_box.height())
        elif self.current_size.width() != self.show_box.width() or self.current_size.height() != self.show_box.height(): 
            self.current_size = QSize(self.show_box.width(), self.show_box.height())


    def handle_area_selected(self, x1, y1, x2, y2):
        print(f"Selected area: x1={x1}, x2={x2}, y1={y1}, y2={y2}")

        if self.original_size is None :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("원본 이미지 사이즈를 인식할 수 없습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()
            return
        elif self.current_size is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("현재 이미지 사이즈를 인식할 수 없습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()
            return
        
        width1 = self.current_size.width()
        height1 = self.current_size.height()
        # 변환할 이미지의 너비와 높이
        width2 = self.original_size.width()
        height2 = self.original_size.height()
        
        # 너비와 높이의 비율 계산
        width_ratio = width2 / width1
        height_ratio = height2 / height1
        
        # 새로운 이미지 크기에 맞게 좌표 변환
        new_x1 = x1 * width_ratio
        new_y1 = y1 * height_ratio
        new_x2 = x2 * width_ratio
        new_y2 = y2 * height_ratio
    
        return new_x1, new_y1, new_x2, new_y2
