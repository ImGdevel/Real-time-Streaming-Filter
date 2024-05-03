import sys
from PySide6.QtCore import QPropertyAnimation, QTimer, Qt
from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout
from PySide6.QtGui import QPalette


class Example(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        
        # 위젯 설정
        self.setGeometry(100, 100, 500, 500)

        # 검은색 배경 설정
        sample = QWidget()
        sample.setStyleSheet('background-color: #000;')
        sample.setFixedSize(10,10)
        

        # 애니메이션 만들기
        self.animation = QPropertyAnimation(sample, b"pos")
        self.animation.setDuration(100000)  # 1초

        # 시작 위치 설정
        start_pos = self.pos()

        # 종료 위치 설정
        end_pos = start_pos
        end_pos.setX(start_pos.x() + 300)
        end_pos.setY(start_pos.y() + 300)

        # 애니메이션 설정
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)

        # 애니메이션 시작
        self.animation.start()
        
        layout.addWidget(sample)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
