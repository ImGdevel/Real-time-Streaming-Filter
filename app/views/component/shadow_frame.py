from PySide6.QtWidgets import QApplication, QWidget, QGraphicsDropShadowEffect, QVBoxLayout, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class ShadowWidget(QWidget):
    def __init__(self):
        super().__init__()

        # QGraphicsDropShadowEffect 생성
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(10)  # 흐림 정도 조절
        shadow_effect.setColor(QColor(0, 0, 0, 150))  # 그림자 색상 및 투명도 조절
        shadow_effect.setOffset(5, 5)  # 그림자 위치 조절

        # QGraphicsDropShadowEffect를 위젯에 적용
        self.setGraphicsEffect(shadow_effect)

if __name__ == "__main__":
    app = QApplication([])
    widget = ShadowWidget()
    widget.show()
    app.exec()
