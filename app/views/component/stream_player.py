import sys
from PySide6.QtCore import Qt, Signal, QTimer, QRectF, QSize
from PySide6.QtGui import QImage, QPixmap, QColor, QPainter
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QMessageBox, QSizePolicy

# Assuming Colors and Icons are defined elsewhere
from utils import Colors, Icons
from .focus_detect_select_area import FocusDetectSelectArea

class SpinnerWidget(QLabel):
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
        self.angle = (self.angle + 10) % 360  # 각도를 5도씩 증가시키며 360도에서 다시 0도로
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


class StreamVideoPlayer(QWidget):
    select_focus_signal = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_size: QSize = None
        self.current_size: QSize = None
        self.initUI()

    def initUI(self):
        video_layout = QVBoxLayout()
        video_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stream_info_bar = QWidget()
        self.stream_info_bar.setMaximumWidth(725)
        self.stream_info_bar.setFixedHeight(30)

        self.show_box = QLabel()
        self.show_box.setStyleSheet(f'background-color: {Colors.baseColor01};')
        self.show_box.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.show_box.setMaximumWidth(725)
        self.show_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout for centering the spinner
        show_box_layout = QVBoxLayout(self.show_box)
        show_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # FocusDetectSelectArea를 show_box와 동일한 위치와 크기로 추가
        self.overlay = FocusDetectSelectArea(self.show_box)
        self.overlay.areaSelected.connect(self.handle_area_selected)
        self.overlay.raise_()

        self.spinner = SpinnerWidget(self.show_box)
        self.spinner.raise_()

        show_box_layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        video_layout.addWidget(self.show_box)
        self.setLayout(video_layout)

    def start_loading(self):
        """로딩 시작"""
        self.spinner.start()

    def stop_loading(self):
        """로딩 멈추기"""
        self.spinner.stop()

    def setFocusSelectMode(self, mode):
        self.overlay.setFocusSelectMode(mode)

    def clearFocusBox(self):
        self.overlay.clearDrawing()

    def setOverlaySize(self):
        """overlay의 크기를 재 설정"""
        
        scaled_image = self.show_box.pixmap()
        if scaled_image.isNull():
            return
        # 현재 show_box의 크기와 이미지의 크기를 비교하여 오프셋을 계산합니다.
        offset_x = (self.show_box.width() - scaled_image.width()) // 2
        offset_y = (self.show_box.height() - scaled_image.height()) // 2

        print("영역:", offset_x, offset_y, scaled_image.width(), scaled_image.height())

        # 새로운 크기 설정
        self.overlay.setGeometry(offset_x, offset_y, scaled_image.width(), scaled_image.height())

    def update_video(self, frame: QImage = None):
        '''비디오 업데이트 메서드'''
        if frame is None or frame.isNull():
            self.frame_clear()
            self.stop_loading()
            return
        if self.spinner.is_spin:
            self.stop_loading()

        self.original_size = frame.size()
        
        pixmap = QPixmap.fromImage(frame)
        scaled_image = pixmap.scaled(self.show_box.width(), self.show_box.height(), Qt.KeepAspectRatio,  Qt.SmoothTransformation)
        self.show_box.setPixmap(scaled_image)

        if self.current_size is None:
            self.current_size = QSize(scaled_image.width(), scaled_image.height())
            self.setOverlaySize()
        elif self.current_size.width() != scaled_image.width() or self.current_size.height() != scaled_image.height():
            self.current_size = QSize(scaled_image.width(), scaled_image.height())
            self.setOverlaySize()

    def frame_clear(self):
        empty_frame = QImage(10, 10, QImage.Format_RGB888)
        empty_frame.fill(QColor(23, 26, 30))
        pixmap = QPixmap.fromImage(empty_frame)
        scaled_image = pixmap.scaled(self.show_box.width(), self.show_box.height(), Qt.KeepAspectRatio,  Qt.SmoothTransformation)
        self.show_box.setPixmap(scaled_image)
        self.clearFocusBox()

    def handle_area_selected(self, x1, y1, x2, y2):
        if x1 is None or  y1 is None or x2 is None or y2 is None or (x2 == 0 and y2 == 0):
            self.select_focus_signal.emit(None)
            return

        print(f"Selected area: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

        if self.original_size is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("원본 이미지 사이즈를 인식할 수 없습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()
            return
        elif self.current_size is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
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

        self.overlay.setFocusSelectMode(False)

        print(f"실제 비율: width ", self.original_size.width() , "hight" , self.original_size.height())
        print(f"실제 웹캠 비율 전환 : x1={new_x1}, y1={new_y1}, x2={new_x2}, y2={new_y2}")

        self.select_focus_signal.emit((int(new_x1), int(new_y1), int(new_x2), int(new_y2)))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setOverlaySize()
