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
        self.focusSelectMode = False
        self.setStyleSheet("background: transparent;")

    def setFocusSelectMode(self, mode):
        self.focusSelectMode = mode

    def clearDrawing(self):
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.update()

    def mousePressEvent(self, event):
        if not self.focusSelectMode:
            return
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if not self.focusSelectMode:
            return
        if self.drawing:
            # 현재 이벤트의 위치를 가져옴
            current_pos = event.pos()
            # 영역 내에 있는지 확인
            if self.rect().contains(current_pos):
                self.end_point = current_pos
                self.update()

    def mouseReleaseEvent(self, event):
        if not self.focusSelectMode:
            return
        if event.button() == Qt.LeftButton:
            # 현재 이벤트의 위치를 가져옴
            current_pos = event.pos()
            # 영역 내에 있는지 확인
            if self.rect().contains(current_pos):
                self.end_point = current_pos
                self.drawing = False
                self.update()

                # 사각형의 좌표 계산 및 신호 발신
                x1 = min(self.start_point.x(), self.end_point.x())
                x2 = max(self.start_point.x(), self.end_point.x())
                y1 = min(self.start_point.y(), self.end_point.y())
                y2 = max(self.start_point.y(), self.end_point.y())

                if x1 == x2 or y1 == y2:
                    self.clearDrawing()
                    return

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
