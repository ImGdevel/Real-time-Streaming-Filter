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
        self.rect_relative = QRect()
        self.setStyleSheet("background: transparent;")
        self.last_size = self.size()

    def setFocusSelectMode(self, mode):
        self.focusSelectMode = mode

    def clearDrawing(self):
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.rect_relative = QRect()
        self.update()

    def isRectValid(self, rect):
        return rect.width() > 0 and rect.height() > 0

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
            current_pos = event.pos()
            if self.rect().contains(current_pos):
                self.end_point = current_pos
                self.update()

    def mouseReleaseEvent(self, event):
        if not self.focusSelectMode:
            return
        if event.button() == Qt.LeftButton:
            current_pos = event.pos()
            if self.rect().contains(current_pos):
                self.end_point = current_pos
                self.drawing = False
                self.update()

                x1 = min(self.start_point.x(), self.end_point.x())
                x2 = max(self.start_point.x(), self.end_point.x())
                y1 = min(self.start_point.y(), self.end_point.y())
                y2 = max(self.start_point.y(), self.end_point.y())

                if x1 == x2 or y1 == y2:
                    self.clearDrawing()
                    return

                self.rect_relative = QRect(x1, y1, x2 - x1, y2 - y1)
                self.last_size = self.size()
                self.areaSelected.emit(x1, y1, x2, y2)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.drawing or not self.start_point.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            
            scaled_rect = QRect(self.start_point, self.end_point)

            current_size = self.size()
            if not self.drawing and self.isRectValid(self.rect_relative) and not self.last_size.isNull():
                width_ratio = current_size.width() / self.last_size.width()
                height_ratio = current_size.height() / self.last_size.height()

                scaled_rect = QRect(
                    int(self.rect_relative.x() * width_ratio),
                    int(self.rect_relative.y() * height_ratio),
                    int(self.rect_relative.width() * width_ratio),
                    int(self.rect_relative.height() * height_ratio)
                )
            else:
                #scaled_rect = self.rect_relative
                scaled_rect = QRect(self.start_point, self.end_point)
            
            painter.drawRect(scaled_rect)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()
