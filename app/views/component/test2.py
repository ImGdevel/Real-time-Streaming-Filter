from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # 버튼 및 위젯 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.resize(600, 600)
        layout.setAlignment(Qt.AlignTop)

        # 붉은 위젯 생성
        self.item = QWidget(self)
        self.item.setStyleSheet("background-color:red;border-radius:15px;")
        self.item.setMinimumSize(50, 50)
        self.item.setMaximumSize(100, 100)
        layout.addWidget(self.item)

        # 애니메이션 생성
        self.shrink_anim = QPropertyAnimation(self.item, b"geometry")
        self.shrink_anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.shrink_anim.setDuration(500)

        self.expand_anim = QPropertyAnimation(self.item, b"geometry")
        self.expand_anim.setEasingCurve(QEasingCurve.InOutQuart)
        self.expand_anim.setDuration(500)

        # 토글 버튼 생성
        self.toggle_button = QPushButton("축소")
        self.toggle_button.setCheckable(True)
        self.toggle_button.toggled.connect(self.toggle_animation)
        layout.addWidget(self.toggle_button)

    def toggle_animation(self, checked):
        # 버튼 상태에 따라 적절한 애니메이션 시작
        if checked:
            # 버튼 선택됨 (축소)
            self.shrink_anim.setStartValue(self.item.geometry())  # 현재 지오메트리 가져오기
            self.shrink_anim.setEndValue(QRect(0, 0, 50, 50))
            self.shrink_anim.start()
            self.toggle_button.setText("확대")
        else:
            # 버튼 선택 해제됨 (확대)
            self.expand_anim.setStartValue(self.item.geometry())  # 현재 지오메트리 가져오기
            self.expand_anim.setEndValue(QRect(0, 0, 100, 100))
            self.expand_anim.start()
            self.toggle_button.setText("축소")

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
