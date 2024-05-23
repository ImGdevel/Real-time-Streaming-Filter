from PySide6.QtWidgets import QWidget, QToolTip
from PySide6.QtGui import QPainter, QBrush, QPen, QFont, QColor
from PySide6.QtCore import Qt, QRect
from utils import Colors

class HelpIconWidget(QWidget):
    def __init__(self, icon_size: int = 20):
        super().__init__()
        self.icon_size = icon_size
        self.comment = ""
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(self.icon_size, self.icon_size)  # 위젯 크기 설정

    def set_text(self, comment: str = ""):
        self.comment = comment
        self.setToolTip(comment)  # 기본 툴팁 설정

    def paintEvent(self, event):
        painter = QPainter(self)

        # 원형 배경 그리기
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(44, 49, 58))  # 원형 배경색을 회색으로 설정
        painter.setBrush(brush)
        pen = QPen(QColor(91, 101, 124))  # 원형 테두리 색을 밝은 회색으로 설정
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawEllipse(0, 0, self.icon_size, self.icon_size)  # 원형 위치와 크기 설정

        # 물음표 그리기
        font = QFont('Arial', int(self.icon_size // 1.5))
        painter.setFont(font)
        painter.setPen(QPen(QColor(91, 101, 124)))  # 물음표 색을 밝은 회색으로 설정
        painter.drawText(QRect(0, 0, self.icon_size, self.icon_size), Qt.AlignCenter, '?')  # 물음표를 가운데에 정렬

    def enterEvent(self, event):
        QToolTip.showText(event.globalPos(), self.comment, self)

    def leaveEvent(self, event):
        QToolTip.hideText()
