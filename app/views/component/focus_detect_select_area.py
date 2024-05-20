from PySide6.QtCore import Qt, QPoint, QRect, Signal
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QLabel

class FocusDetectSelectArea(QLabel):
    areaSelected = Signal(int, int, int, int)  # 좌표를 전달하는 신호 정의

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.drawing = False
        self.setStyleSheet("background: transparent;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = event.pos()
            self.drawing = False
            self.update()

            # 사각형의 좌표 계산 및 신호 발신
            x1 = min(self.start_point.x(), self.end_point.x())
            x2 = max(self.start_point.x(), self.end_point.x())
            y1 = min(self.start_point.y(), self.end_point.y())
            y2 = max(self.start_point.y(), self.end_point.y())
            self.areaSelected.emit(x1, y1, x2, y2)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.drawing or not self.start_point.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            rect = QRect(self.start_point, self.end_point)
            painter.drawRect(rect)
